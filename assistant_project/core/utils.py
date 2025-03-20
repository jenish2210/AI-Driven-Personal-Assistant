import speech_recognition as sr

def process_voice_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for command...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio)
            print(f"Command: {command}")
            return command
        except sr.UnknownValueError:
            return "Sorry, I couldn't understand that."
        except sr.RequestError as e:
            return f"API error: {e}"


# import pyttsx3
# import logging

# # Set up logging to track errors
# logging.basicConfig(level=logging.INFO, filename='tts_errors.log', format='%(asctime)s - %(message)s')

# def speak(text, voice_id=None, rate=150, volume=0.9):
#     """
#     Convert text to speech with customizable voice, rate, and volume, and handle errors.

#     Args:
#         text (str): The text to convert to speech.
#         voice_id (str): Specific voice ID to use (optional).
#         rate (int): Speed of speech.
#         volume (float): Volume level.
#     """
#     try:
#         # Initialize the TTS engine
#         engine = pyttsx3.init()

#         # Set the speech rate and volume
#         engine.setProperty('rate', rate)
#         engine.setProperty('volume', volume)

#         # Set a specific voice by ID if provided
#         if voice_id:
#             engine.setProperty('voice', voice_id)

#         # Start speaking the text
#         engine.say(text)
#         engine.runAndWait()

#     except pyttsx3.gtts.tts.gTTSError as e:
#         logging.error(f"gTTS Error: {str(e)}")
#         print("Error: Unable to convert speech using gTTS.")
    
#     except pyttsx3.voice.voice_error as e:
#         logging.error(f"Voice Error: {str(e)}")
#         print("Error: Selected voice not available.")
    
#     except Exception as e:
#         logging.error(f"General Error: {str(e)}")
#         print(f"Error: An unexpected error occurred. Details: {str(e)}")

# from core.utils import speak
# if __name__ == "__main__":
#     speak("Hello Jenish! How can I assist you today?")

#     speak("You have a meeting scheduled at 3 PM.")
#     speak("Please take your medication now.")


#==============================================================================================================================


import os
import time
import pygame
from gtts import gTTS

def speak(text):
    """Convert text to speech and play it using pygame."""
    
    # Generate a unique filename (timestamp-based)
    filename = f"tts_{int(time.time())}.mp3"

    # Convert text to speech
    tts = gTTS(text=text, lang='en')
    tts.save(filename)

    # Initialize pygame mixer
    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()

    # Wait for the speech to finish
    while pygame.mixer.music.get_busy():
        time.sleep(0.1)

    # Delete the file after playing
    os.remove(filename)


#====================================================================

from twilio.rest import Client
from django.conf import settings

def send_msg(to_number, message):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    
    try:
        message = client.messages.create(
            body=message,
            from_=settings.TWILIO_PHONE_NUMBER,
            to=to_number
        )
        return f"Message sent successfully: {message.sid}"
    except Exception as e:
        return f"Error sending message: {str(e)}"


#================================================================

from twilio.rest import Client
from django.conf import settings

def send_sms(to, message):
    """Send an SMS notification."""
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        body=message,
        from_=settings.TWILIO_PHONE_NUMBER,
        to=to  # User's phone number
    )
    return message.sid
