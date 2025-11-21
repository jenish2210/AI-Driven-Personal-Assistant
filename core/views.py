# assistant_project/core/views.py
from rest_framework.viewsets import ModelViewSet
from .models import Reminder, EmergencyContact, Task
from .serializers import ReminderSerializer, EmergencyContactSerializer
from rest_framework import viewsets
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.http import JsonResponse, FileResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

import warnings
import os
import time
import json
import requests

import pyttsx3
from gtts import gTTS
import phonenumbers
from twilio.rest import Client
from datetime import datetime

# ------------------ Lazy import helper for speech_recognition ------------------
_sr = None
_sr_import_attempted = False

def get_speech_recognition():
    """
    Lazy-import speech_recognition. Returns the module or None if import fails.
    Caches the result so repeated imports are not attempted.
    """
    global _sr, _sr_import_attempted
    if _sr_import_attempted:
        return _sr
    _sr_import_attempted = True
    try:
        import speech_recognition as sr
        _sr = sr
    except Exception as e:
        _sr = None
        warnings.warn(f"speech_recognition unavailable: {e}")
    return _sr

# ------------------ ViewSets ------------------
class ReminderViewSet(ModelViewSet):
    """
    API endpoint for managing reminders.
    """
    queryset = Reminder.objects.all()
    serializer_class = ReminderSerializer

class EmergencyContactViewSet(ModelViewSet):
    """
    API endpoint for managing emergency contacts.
    """
    queryset = EmergencyContact.objects.all()
    serializer_class = EmergencyContactSerializer

# ------------------ Speech -> Text view (uses lazy import) ------------------
def speech_to_text_view(request):
    """
    Endpoint to convert speech from the server microphone to text.
    NOTE: Usually servers don't have a microphone. This view will return 503
    if audio features are not available in the environment.
    """
    sr = get_speech_recognition()
    if sr is None:
        return JsonResponse({"error": "Audio features are disabled in this environment."}, status=503)

    # Only proceed for GET (as in your original code). You can change this to POST if you prefer.
    if request.method == "GET":
        recognizer = sr.Recognizer()
        try:
            with sr.Microphone() as source:
                print("Listening...")
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source)
                text = recognizer.recognize_google(audio)
                return JsonResponse({"text": text})
        except sr.UnknownValueError:
            return JsonResponse({"error": "Could not understand the audio."})
        except sr.RequestError:
            return JsonResponse({"error": "Could not request results. Check your internet connection."})
        except Exception as e:
            # Catch-all to avoid crashing the server if microphone isn't usable
            return JsonResponse({"error": f"Audio capture failed: {str(e)}"}, status=500)

    return render(request, "speech_to_text.html")

# ------------------ Text -> Speech (pyttsx3) ------------------
def text_to_speech_view(request):
    print("View accessed!")  # Debugging line
    if request.method == "POST":
        text = request.POST.get("text", "Please enter some text.")
        print(f"Text received: {text}")
        try:
            engine = pyttsx3.init()
            engine.say(text)
            engine.runAndWait()
            return JsonResponse({"message": "Speech generated successfully"})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return render(request, "text_to_speech.html")

# ------------------ Simple voice command API placeholder ------------------
def voice_command_view(request):
    return JsonResponse({'message': 'Voice command processed successfully!'})

# ------------------ List available TTS voices ------------------
def list_voices_view(request):
    """
    API endpoint to list all available TTS voices.
    """
    try:
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')

        voice_details = []
        for voice in voices:
            # voice.languages can be bytes or list depending on platform; handle both safely
            langs = []
            try:
                if hasattr(voice, "languages") and voice.languages:
                    for lang in voice.languages:
                        if isinstance(lang, bytes):
                            try:
                                langs.append(lang.decode('utf-8'))
                            except Exception:
                                langs.append(str(lang))
                        else:
                            langs.append(str(lang))
            except Exception:
                langs = []

            voice_details.append({
                'id': getattr(voice, 'id', ''),
                'name': getattr(voice, 'name', ''),
                'gender': getattr(voice, 'gender', None),
                'languages': langs,
            })

        return JsonResponse({'voices': voice_details})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# ------------------ Customized TTS using gTTS (returns file) ------------------
def customized_tts_view(request):
    """Django view to generate and serve speech audio."""
    text = request.GET.get('text', "Hello! How can I assist you today?")
    filename = f"tts_{int(time.time())}.mp3"
    media_dir = "media"
    os.makedirs(media_dir, exist_ok=True)
    filepath = os.path.join(media_dir, filename)

    try:
        tts = gTTS(text=text, lang='en')
        tts.save(filepath)
        return FileResponse(open(filepath, "rb"), content_type="audio/mpeg", as_attachment=True, filename=filename)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

# ------------------ speak helper (pyttsx3) ------------------
def speak(text, voice_id=None, rate=150, volume=0.9):
    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', rate)
        engine.setProperty('volume', volume)
        if voice_id:
            engine.setProperty('voice', voice_id)
        else:
            voices = engine.getProperty('voices')
            if voices:
                engine.setProperty('voice', voices[0].id)
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        # Logging here is preferable in a real app
        print(f"Error in TTS: {e}")

# ------------------ Keyboard shortcuts starter ------------------
from .accessibility import setup_keyboard_shortcuts

def start_keyboard_listener(request):
    setup_keyboard_shortcuts()
    return HttpResponse("Keyboard listener started.")

# ------------------ Theme/save preference ------------------
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

# ------------------ Simple TTS page ------------------
def tts_page(request):
    return HttpResponse("Text-to-Speech Page")

# ------------------ Twilio helpers & emergency alert ------------------
def send_sms(phone_number, message):
    # IMPORTANT: Move these credentials to environment variables before deploying
    TWILIO_ACCOUNT_SID = "ACbbc929b41e85afc1bc852ed7c14c5cb2"
    TWILIO_AUTH_TOKEN = "bad0002b4e42c9b0f5bf7e2333c18126"
    TWILIO_PHONE_NUMBER = "+18562927234"

    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        message_obj = client.messages.create(
            body=message,
            from_=TWILIO_PHONE_NUMBER,
            to=phone_number
        )
        return {"status": "Message sent successfully!", "sid": message_obj.sid}
    except Exception as e:
        return {"error": str(e)}

def emergency_alert(request):
    emergency_number = "+919043949382"
    message = "This is an emergency alert. Please respond immediately!"
    response_data = send_sms(emergency_number, message)
    return JsonResponse(response_data)

# ------------------ Location endpoints ------------------
@csrf_exempt
def location_page(request):
    return render(request, "location.html")

@csrf_exempt
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

# ------------------ send_msg via Twilio with phonenumbers validation ------------------
def send_msg(request):
    TWILIO_ACCOUNT_SID = "ACbbc929b41e85afc1bc852ed7c14c5cb2"
    TWILIO_AUTH_TOKEN = "bad0002b4e42c9b0f5bf7e2333c18126"
    TWILIO_PHONE_NUMBER = "+18562927234"
    recipient_number = "+919043949382"

    try:
        parsed_number = phonenumbers.parse(recipient_number, None)
        if not phonenumbers.is_valid_number(parsed_number):
            return JsonResponse({"error": "Invalid phone number format."})

        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        message_obj = client.messages.create(
            body="Hello, this is a test message!",
            from_=TWILIO_PHONE_NUMBER,
            to=recipient_number
        )
        return JsonResponse({"status": "Message sent successfully!", "sid": message_obj.sid})
    except Exception as e:
        return JsonResponse({"error": str(e)})

# ------------------ Reminders CRUD and task manager ------------------
def add_reminder(request):
    if request.method == "POST":
        reminder_text = request.POST.get("reminder_text", "")
        reminder_time = request.POST.get("reminder_time", "")
        if reminder_text and reminder_time:
            reminder_time = datetime.strptime(reminder_time, "%Y-%m-%dT%H:%M")
            reminder = Reminder.objects.create(text=reminder_text, time=reminder_time)
            return JsonResponse({"message": "Reminder added!", "reminder": {
                "text": reminder.text,
                "time": reminder.time.strftime("%Y-%m-%d %H:%M")
            }})
    reminders = Reminder.objects.all().order_by("time")
    return render(request, "home.html", {"reminders": reminders})

def delete_reminder(request, reminder_id):
    try:
        reminder = Reminder.objects.get(id=reminder_id)
        reminder.delete()
        return JsonResponse({"message": "Reminder deleted successfully!"})
    except Reminder.DoesNotExist:
        return JsonResponse({"error": "Reminder not found!"}, status=404)

def get_reminders(request):
    reminders = list(Reminder.objects.values())
    return JsonResponse({"reminders": reminders})

# ------------------ Simple chatbot (Gemini) ------------------
GEMINI_API_KEY = "AIzaSyCFiPRO_jSXOZH5gnMvKE98SzsGu_6O-Tk"

@csrf_exempt
def chatbot(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))
            user_message = data.get("user_input", "")
            gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"
            headers = {"Content-Type": "application/json"}
            payload = {"contents": [{"parts": [{"text": user_message}]}]}
            response = requests.post(gemini_url, headers=headers, json=payload)
            response_data = response.json()
            bot_response = response_data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "Sorry, I didn't understand that.")
            return JsonResponse({"response": bot_response})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return render(request, "chat.html")

# ------------------ Home and task manager views ------------------
def home(request):
    return render(request, "home.html")

@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user)
    return render(request, 'tasks/task_list.html', {'tasks': tasks})

@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'tasks/task_form.html', {'form': form})

@login_required
def task_update(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/task_form.html', {'form': form})

@login_required
def task_delete(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('task_list')
    return render(request, 'tasks/task_confirm_delete.html', {'task': task})

def task_manager(request):
    return render(request, 'task_manager.html')

def add_task(request):
    if request.method == "POST":
        title = request.POST.get("title")
        priority = request.POST.get("priority", 1)
        try:
            priority = int(priority)
        except ValueError:
            priority = 1
        Task.objects.create(title=title, priority=priority, completed=False)
        return redirect("task_manager")
    return render(request, "add_task.html")

def complete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.completed = True
    task.save()
    return redirect("task_manager")

def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    return redirect("task_manager")
