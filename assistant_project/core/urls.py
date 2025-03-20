from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ReminderViewSet, customized_tts_view, text_to_speech_view  # Import the ViewSet directly



router = DefaultRouter()
router.register(r'reminders', ReminderViewSet)  # Register ViewSet here

# urlpatterns = [
#     path('', include(router.urls)),
#   # Include router URLs
# ]


from rest_framework.routers import DefaultRouter
from .views import ReminderViewSet, EmergencyContactViewSet

# Create a router to manage API routes
router = DefaultRouter()
router.register(r'reminders', ReminderViewSet)  # Register the ReminderViewSet
router.register(r'contacts', EmergencyContactViewSet)  # Register the EmergencyContactViewSet

# Define the urlpatterns using the router
urlpatterns = router.urls

import speech_recognition as sr

def process_voice_command(requst):
    """
    Captures audio input from the user's microphone and converts it to text.
    """
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("Adjusting for ambient noise. Please wait...")
            recognizer.adjust_for_ambient_noise(source)  # Adjust for noise
            print("Listening for your voice command...")
            audio = recognizer.listen(source)  # Capture the audio

            # Use Google's Speech Recognition API to convert speech to text
            command = recognizer.recognize_google(audio)
            print(f"Recognized Command: {command}")
            return command
    except sr.UnknownValueError:
        # Handle cases where the speech was unclear
        return "Sorry, I couldn't understand that. Please try again."
    except sr.RequestError as e:
        # Handle issues with the API or service
        return f"Could not request results from Google Speech Recognition service: {e}"



from django.urls import path
from .views import *

from .views import customized_tts_view
from .views import text_to_speech_view

from .views import speech_to_text_view
from django.urls import path
from .views import emergency_alert

from django.urls import path
from .views import emergency_alert


from .views import add_reminder

from .views import chatbot



urlpatterns = [
    path('text_to_speech/', text_to_speech_view),
    path('voice/', voice_command_view),
    path('speech/', speech_to_text_view),
    path('list_voices/', list_voices_view),
    path('save-theme/', customized_tts_view),
    path('tts/', customized_tts_view),  # API for TTS
    path('send_sms/', send_msg,),
    path("speech-to-text/", speech_to_text_view),
    path('send_alert/', emergency_alert,),
    path('send_location/', receive_location),
    path('add_reminder/', add_reminder),
    # path("chat/", chat_with_huggingface),
    path("chatbot/", chatbot), 
    


]





