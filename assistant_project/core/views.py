from rest_framework.viewsets import ModelViewSet
from .models import Reminder, EmergencyContact
from .serializers import ReminderSerializer, EmergencyContactSerializer
from rest_framework import viewsets
from .models import Reminder
from .serializers import ReminderSerializer
from django.shortcuts import render


class ReminderViewSet(ModelViewSet):
    """
    API endpoint for managing reminders.
    """
    queryset = Reminder.objects.all()  # Fetch all reminders from the database
    serializer_class = ReminderSerializer  # Use ReminderSerializer to handle input/output data

class EmergencyContactViewSet(ModelViewSet):
    """
    API endpoint for managing emergency contacts.
    """
    queryset = EmergencyContact.objects.all()  # Fetch all emergency contacts from the database
    serializer_class = EmergencyContactSerializer  # Use EmergencyContactSerializer for input/output data


#===============================================================================================================
# import speech_recognition as sr
# from django.http import JsonResponse

# def speech_to_text_view(request):
#     recognizer = sr.Recognizer()
    
#     try:
#         with sr.Microphone() as source:
#             print("Listening...")
#             recognizer.adjust_for_ambient_noise(source)
#             audio = recognizer.listen(source)
#             text = recognizer.recognize_google(audio)  # Google Speech API
#             return JsonResponse({"text": text})

#     except sr.UnknownValueError:
#         return JsonResponse({"error": "Could not understand the audio."})
#     except sr.RequestError:
#         return JsonResponse({"error": "Could not request results. Check your internet connection."})

import speech_recognition as sr
from django.http import JsonResponse


def speech_to_text_view(request):
    if request.method == "GET":
        recognizer = sr.Recognizer()
        
        try:
            with sr.Microphone() as source:
                print("Listening...")
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source)
                text = recognizer.recognize_google(audio)  # Google Speech API
                return JsonResponse({"text": text})

        except sr.UnknownValueError:
            return JsonResponse({"error": "Could not understand the audio."})
        except sr.RequestError:
            return JsonResponse({"error": "Could not request results. Check your internet connection."})
    
    # return JsonResponse({"error": "Invalid request method."})
    return render(request, "speech_to_text.html")
    


#=============================================================================================================================

# from django.http import JsonResponse
# # from .utils import list_voices
# from .utils import speak  # Replace with the correct function name
# import pyttsx3

# from django.http import JsonResponse
# import pyttsx3

# def text_to_speech_view(request):
#     text = request.GET.get("text", "Hello, this is a default response.")
    
#     """
#     API endpoint to handle text-to-speech and return captions.
#     """
#     try:
#         text = request.GET.get('text', "Hello! Welcome to the AI Assistant.")
#         captions_enabled = request.GET.get('display_captions', 'true').lower() == 'true'

#         # Use pyttsx3 for Text-to-Speech
#         engine = pyttsx3.init()
#         engine.say(text)
#         engine.runAndWait()

#         # Return the response as JSON
#         return JsonResponse({
#             "status": "success",
#             "text": text if captions_enabled else "",
#             "captions_enabled": captions_enabled,
#         })
#     except Exception as e:
#         return JsonResponse({"status": "error", "message": str(e)}, status=500)


from django.shortcuts import render
from django.http import JsonResponse
import pyttsx3
# def text_to_speech_view(request):
#     return render(request, "text_to_speech.html")
def text_to_speech_view(request):
    if request.method == "POST":
        text = request.POST.get("text", "Please enter some text.")  # Get input from user
    
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()

        return JsonResponse({"message": "Speech generated successfully"})

    return render(request, "text_to_speech.html")  # Render HTML page for user input


#========================================================================================================================================


# def voice_command_view(request):
#     return render(request, 'voice_command/index.html')
def voice_command_view(request):
    return JsonResponse({'message': 'Voice command processed successfully!'})

from django.shortcuts import render


def list_voices_view(request):
    
    """
    API endpoint to list all available TTS voices.
    """
    import pyttsx3
    
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    
    voice_details = []
    for voice in voices:
        voice_details.append({
            'id': voice.id,
            'name': voice.name,
            'gender': voice.gender,
            'languages': voice.languages,
        })
    
    return JsonResponse({'voices': voice_details})

#=============================================================================================================================

# from django.shortcuts import render
# from django.http import JsonResponse
# import pyttsx3  # Python text-to-speech engine

# def tts_page(request):
#     """Render the webpage with the text-to-speech interface."""
#     return render(request, 'tts.html')

# def customized_tts_view(request):
#     """API endpoint to convert text to speech with custom settings."""
#     text = request.GET.get('text', "Hello! How can I assist you today?")
#     voice_type = request.GET.get('voice_type', 'female')  # Default: female
#     rate = int(request.GET.get('rate', 150))  # Default: 150
#     volume = float(request.GET.get('volume', 0.9))  # Default: 0.9

#     # Initialize TTS engine
#     engine = pyttsx3.init()

#     # Set voice type
#     voices = engine.getProperty('voices')
#     if voice_type.lower() == 'male':
#         engine.setProperty('voice', voices[0].id)  # Male voice
#     else:
#         engine.setProperty('voice', voices[1].id)  # Female voice

#     # Set speech properties
#     engine.setProperty('rate', rate)
#     engine.setProperty('volume', volume)

#     # Speak the text
#     engine.say(text)
#     engine.runAndWait()

#     return JsonResponse({
#         "message": "Speech played successfully.",
#         "settings": {
#             "text": text,
#             "voice_type": voice_type,
#             "rate": rate,
#             "volume": volume,
#         }
#     })

from django.http import JsonResponse, FileResponse
import os
import time
from gtts import gTTS

def customized_tts_view(request):
    """Django view to generate and serve speech audio."""
    
    text = request.GET.get('text', "Hello! How can I assist you today?")
    
    # Generate a unique filename
    filename = f"tts_{int(time.time())}.mp3"
    filepath = os.path.join("media", filename)  # Save in media directory

    # Convert text to speech
    tts = gTTS(text=text, lang='en')
    tts.save(filepath)

    # Return the audio file as response
    return FileResponse(open(filepath, "rb"), content_type="audio/mpeg", as_attachment=True, filename=filename)



#===============================================================================================================================

import pyttsx3

def speak(text, voice_id=None, rate=150, volume=0.9):
    """
    Convert text to speech with customizable voice, rate, and volume.

    Args:
        text (str): The text to convert to speech.
        voice_id (str): Specific voice ID to use (optional).
        rate (int): Speed of speech (default: 150 words per minute).
        volume (float): Volume level (default: 0.9, range: 0.0 to 1.0).
    """
    try:
        # Initialize the pyttsx3 engine
        engine = pyttsx3.init()

        # Set speech rate
        engine.setProperty('rate', rate)

        # Set volume
        engine.setProperty('volume', volume)

        # If a specific voice_id is provided, set the voice to that ID
        if voice_id:
            engine.setProperty('voice', voice_id)
        else:
            # Use the default voice if no voice_id is provided
            engine.setProperty('voice', engine.getProperty('voices')[0].id)  # Default to the first available voice

        # Speak the provided text
        engine.say(text)
        engine.runAndWait()

    except Exception as e:
        print(f"Error in TTS: {e}")

#===============================================================================================================================
from django.http import HttpResponse
from .accessibility import setup_keyboard_shortcuts

def start_keyboard_listener(request):
    setup_keyboard_shortcuts()
    return HttpResponse("Keyboard listener started.")










# from django.http import JsonResponse
# from .utils import list_voices


# def list_voices_view(request):
#     """
#     API endpoint to list all available TTS voices.
#     """
#     import pyttsx3
    
#     engine = pyttsx3.init()
#     voices = engine.getProperty('voices')
    
#     voice_details = []
#     for voice in voices:
#         voice_details.append({
#             'id': voice.id,  # Registry path
#             'name': voice.name,  # Friendly name
#             'gender': voice.gender if voice.gender else 'Unknown',  # Gender info (if available)
#             'language': voice.languages[0] if voice.languages else 'Unknown',  # Language (if available)
#         })
    
#     return JsonResponse({'voices': voice_details})



# except ValueError as e:
#         # Handle errors related to invalid values in parameters
#         return JsonResponse({"error": f"Invalid value in parameters: {str(e)}"}, status=400)

#     except Exception as e:
#         # Handle general errors
#         return JsonResponse({"error": f"An unexpected error occurred: {str(e)}"}, status=500)



from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

@login_required
def save_theme_preference(request):
    theme = request.POST.get('theme', 'default')
    user_profile = request.user.profile  # Access the related UserProfile
    user_profile.theme_preference = theme
    user_profile.save()
    return JsonResponse({'status': 'success', 'theme': theme})

def index(request):
    user_theme = request.user.profile.theme_preference if request.user.is_authenticated else 'default'
    return render(request, 'index.html', {'user_theme': user_theme})




def list_voices():
    """
    List all available voices with details.

    Returns:
        List[Dict]: A list of dictionaries containing voice details (id, name, gender, and language).
    """
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')

    voice_details = []
    for index, voice in enumerate(voices):
        voice_details.append({
            'id': voice.id,           # Unique ID for the voice
            'name': voice.name,       # Voice name
            'gender': voice.gender,   # Gender of the voice
            'language': voice.languages[0].decode('utf-8') if voice.languages else 'Unknown'  # Language of the voice
        })


#===============================================================================================================


from django.shortcuts import render, HttpResponse

def tts_page(request):
    return HttpResponse("Text-to-Speech Page")



#=================================================================

from twilio.rest import Client
from django.http import JsonResponse

def send_sms(phone_number, message):  # Accepts 2 parameters
    TWILIO_ACCOUNT_SID = "ACbbc929b41e85afc1bc852ed7c14c5cb2"
    TWILIO_AUTH_TOKEN = "912de4a62ed3b7ad7988bc4ddaf62f70"
    TWILIO_PHONE_NUMBER = "+18562927234" # Your Twilio number

    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            body=message,  
            from_=TWILIO_PHONE_NUMBER,
            to=phone_number  
        )
        return {"status": "Message sent successfully!", "sid": message.sid}
    
    except Exception as e:
        return {"error": str(e)}
from django.http import JsonResponse

def emergency_alert(request):
    emergency_number = "+919043949382"  # Replace with actual emergency number
    message = "This is an emergency alert. Please respond immediately!"

    # Pass both parameters correctly
    response_data = send_sms(emergency_number, message)

    return JsonResponse(response_data)  # Convert response to JSON



#===========location=========================

from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
@csrf_exempt
def location_page(request):
    return render(request, "location.html")
def receive_location(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            latitude = data.get("latitude")
            longitude = data.get("longitude")

            if latitude and longitude:
                return JsonResponse({"message": "Location received", "latitude": latitude, "longitude": longitude})
            else:
                return JsonResponse({"error": "Invalid data"}, status=400)
        
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)

    return JsonResponse({"error": "Invalid request"}, status=400)

# #===================================================================================


import phonenumbers
from twilio.rest import Client
from django.http import JsonResponse

def send_msg(request):
    TWILIO_ACCOUNT_SID = "ACbbc929b41e85afc1bc852ed7c14c5cb2"
    TWILIO_AUTH_TOKEN = "912de4a62ed3b7ad7988bc4ddaf62f70"
    TWILIO_PHONE_NUMBER = "+18562927234"  # Your Twilio number

    recipient_number = "+919043949382"  # Replace with user input

    # Validate phone number
    try:
        parsed_number = phonenumbers.parse(recipient_number, None)
        if not phonenumbers.is_valid_number(parsed_number):
            return JsonResponse({"error": "Invalid phone number format."})

        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            body="Hello, this is a test message!",
            from_=TWILIO_PHONE_NUMBER,
            to=recipient_number
        )
        return JsonResponse({"status": "Message sent successfully!", "sid": message.sid})
    
    except Exception as e:
        return JsonResponse({"error": str(e)})


# #=======================================================

from django.shortcuts import render
from django.utils.timezone import make_aware
from datetime import datetime
from .models import Reminder

def add_reminder(request):
    if request.method == "POST":
        message = request.POST.get("message")
        date_str = request.POST.get("date")  # Format: YYYY-MM-DD
        time_str = request.POST.get("time")  # Format: HH:MM

        # Combine date and time
        datetime_str = f"{date_str} {time_str}"
        scheduled_time = make_aware(datetime.strptime(datetime_str, "%Y-%m-%d %H:%M"))

        # Save to the database
        Reminder.objects.create(message=message, scheduled_time=scheduled_time)

        return render(request, "success.html", {"message": "Reminder Set Successfully!"})

    return render(request, "add_reminder.html")

# #================ GPT ======================================================================

import json
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render

GEMINI_API_KEY = "AIzaSyCFiPRO_jSXOZH5gnMvKE98SzsGu_6O-Tk"  # Replace with your API key

@csrf_exempt
def chatbot(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))
            user_message = data.get("user_input", "")

            # Send request to Google Gemini API
            gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"
            headers = {"Content-Type": "application/json"}
            payload = {
                "contents": [{"parts": [{"text": user_message}]}]
            }

            response = requests.post(gemini_url, headers=headers, json=payload)
            response_data = response.json()

            # Extract AI response
            bot_response = response_data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "Sorry, I didn't understand that.")

            return JsonResponse({"response": bot_response})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return render(request, "chat.html")
