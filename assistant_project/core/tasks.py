from apscheduler.schedulers.background import BackgroundScheduler
from django.utils.timezone import now
from .models import Reminder
from .utils import send_sms

def reminder_task():
    """Check for reminders and send SMS notifications."""
    reminders = Reminder.objects.filter(scheduled_time__lte=now())

    for reminder in reminders:
        phone_number = "+919876543210"  # Replace with user's number
        send_sms(phone_number, f"🔔 Reminder: {reminder.message}")

        # Optionally, delete the reminder after sending
        reminder.delete()

# Start the scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(reminder_task, "interval", minutes=1)  # Check every minute
scheduler.start()

