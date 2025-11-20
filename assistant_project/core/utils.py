# assistant_project/core/utils.py
import os
import time
import warnings

# --- Lazy / guarded audio imports ----------------------------------------
try:
    import speech_recognition as sr  # may fail in some environments
except Exception as e:
    sr = None
    warnings.warn(
        "speech_recognition is not available (audio features disabled). "
        f"Import error: {e}",
        RuntimeWarning
    )

# pydub is optional (used in some audio flows) — guard it
try:
    import pydub
except Exception:
    pydub = None

# Do not import or initialize pygame at module import time (can hang on servers).
# We'll import it inside the speak() function when needed.

# --- Voice recognition (microphone) --------------------------------------
def process_voice_command(timeout=5, phrase_time_limit=8):
    """
    Listen on the default microphone and return the recognized text.
    If speech_recognition (sr) is unavailable, returns a helpful message.
    """
    if sr is None:
        return "Audio recognition is disabled on this environment."

    try:
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening for command...")
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            try:
                command = recognizer.recognize_google(audio)
                print(f"Command: {command}")
                return command
            except sr.UnknownValueError:
                return "Sorry, I couldn't understand that."
            except sr.RequestError as e:
                return f"API error: {e}"
    except Exception as e:
        # Could be a microphone / OS error — return friendly text, but don't crash app.
        warnings.warn(f"Microphone/recognition error: {e}", RuntimeWarning)
        return f"Audio recognition error: {e}"

# --- Text-to-Speech (TTS) ------------------------------------------------
def speak(text, lang="en"):
    """
    Convert text to speech and attempt to play it.
    This function tries to import gTTS and pygame when called.
    If playback is not possible, it will save the audio file and then remove it.
    """
    # Lazy import of gTTS
    try:
        from gtts import gTTS
    except Exception as e:
        warnings.warn(f"gTTS not available: {e}", RuntimeWarning)
        # fallback: just print the text so user sees output
        print("[TTS disabled] " + text)
        return

    # create a temporary filename
    filename = f"tts_{int(time.time())}.mp3"
    try:
        tts = gTTS(text=text, lang=lang)
        tts.save(filename)
    except Exception as e:
        warnings.warn(f"Failed to generate TTS audio: {e}", RuntimeWarning)
        return

    # Try to play with pygame if available
    try:
        import pygame
        # Initialize mixer lazily and play
        try:
            pygame.mixer.init()
            pygame.mixer.music.load(filename)
            pygame.mixer.music.play()
            # Wait until playback finishes
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
        finally:
            # Quit mixer to free audio device
            try:
                pygame.mixer.quit()
            except Exception:
                pass
    except Exception as e:
        # If pygame is not available or playback fails, just notify and keep file momentarily.
        warnings.warn(f"pygame playback failed or not available: {e}", RuntimeWarning)
        print(f"[TTS saved to file] {filename} (playback skipped)")

    # Clean up the audio file if it exists
    try:
        if os.path.exists(filename):
            os.remove(filename)
    except Exception as e:
        warnings.warn(f"Failed to remove temp TTS file {filename}: {e}", RuntimeWarning)


# --- Twilio SMS helper ---------------------------------------------------
def send_sms(to_number, message_body):
    """
    Send an SMS using Twilio. Uses Django settings for credentials.
    Returns the message SID on success or an error message on failure.
    """
    try:
        # Import Twilio client lazily to avoid import-time issues
        from twilio.rest import Client
        from django.conf import settings
    except Exception as e:
        return f"Twilio or Django settings not available: {e}"

    try:
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            body=message_body,
            from_=settings.TWILIO_PHONE_NUMBER,
            to=to_number
        )
        return message.sid
    except Exception as e:
        return f"Error sending message: {str(e)}"


# --- small helper to check audio availability ----------------------------
def audio_available():
    """Return True if any audio libraries appear to be usable."""
    # We consider speech_recognition or pydub availability as a proxy.
    return sr is not None or pydub is not None
