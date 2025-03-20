from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from .utils import speak

def reminder_task():
    """
    Task to remind the user. This can be customized to announce anything.
    """
    current_time = datetime.now().strftime("%H:%M:%S")
    speak(f"Reminder! The current time is {current_time}")
    speak("It's time to take your medication.")

def start_scheduler():
    """
    Starts the APScheduler to schedule the reminders.
    """
    scheduler = BackgroundScheduler()

    # Schedule the reminder task to run every 30 seconds
    scheduler.add_job(
        func=reminder_task,
        trigger="cron",  # Use cron for specific times
        hour=9,  # 9 AM every day
        minute=0,
        id="daily_reminder"
)

    

    scheduler.start()
    #scheduler.shutdown()

