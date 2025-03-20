import pyttsx3

def speak(text, voice_type='female', rate=150, volume=0.9):
    """
    Convert text to speech with customizable settings.

    Args:
        text (str): The text to convert to speech.
        voice_type (str): The desired voice type ('male' or 'female').
        rate (int): The speed of speech (default: 150 words per minute).
        volume (float): The volume level (default: 0.9, range: 0.0 to 1.0).
    """
    engine = pyttsx3.init()

    # Get available voices
    voices = engine.getProperty('voices')

    # Set voice: Male or Female
    if voice_type.lower() == 'male':
        engine.setProperty('voice', voices[0].id)  # Usually, male voice is at index 0
    elif voice_type.lower() == 'female':
        engine.setProperty('voice', voices[1].id)  # Female voice is at index 1
    else:
        print("Invalid voice type. Defaulting to female voice.")
        engine.setProperty('voice', voices[1].id)

    # Set speaking rate
    engine.setProperty('rate', rate)

    # Set volume
    engine.setProperty('volume', volume)

    # Speak the text
    engine.say(text)
    engine.runAndWait()

# Test the function
if __name__ == "__main__":
    # Example 1: Female voice, slower rate, lower volume
    speak("Hello! How can I assist you today?", voice_type='female', rate=150, volume=0.7)

    # Example 2: Male voice, faster rate, louder volume
    speak("Good morning! I am here to help you.", voice_type='male', rate=200, volume=1.0)

from core.utils import speak

# Female voice, slower rate, moderate volume
speak("Hello! Welcome to the TTS demo.", voice_type='female', rate=120, volume=0.8)

# Male voice, faster rate, louder volume
speak("How can I assist you today?", voice_type='male', rate=200, volume=1.0)
