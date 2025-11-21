# core/scheduler.py
import logging

logger = logging.getLogger(__name__)

def reminder_task():
    """
    Task to remind the user. This can be customized to announce anything.
    """
    from datetime import datetime
    try:
        # lazy import speak so scheduler module can be imported without TTS libs
        from .utils import speak
    except Exception:
        # fallback: just log if speak() isn't available
        speak = None

    current_time = datetime.now().strftime("%H:%M:%S")
    msg = f"Reminder! The current time is {current_time}"
    if speak:
        try:
            speak(msg)
            speak("It's time to take your medication.")
        except Exception as e:
            logger.exception("speak() failed in reminder_task: %s", e)
    else:
        logger.info("Reminder (no speak available): %s", msg)
        logger.info("It's time to take your medication.")

def start_scheduler(skip_test_job: bool = True):
    """
    Starts the APScheduler to schedule the reminders.

    - skip_test_job: if False, also schedules a very-frequent test job (every 30s).
      Keep True in production.
    Returns the scheduler instance (or None if apscheduler isn't available).
    """
    try:
        # lazy imports so importing this module doesn't require apscheduler
        from apscheduler.schedulers.background import BackgroundScheduler
        from apscheduler.triggers.cron import CronTrigger
        from apscheduler.triggers.interval import IntervalTrigger
    except ImportError:
        logger.exception("apscheduler is not installed. Scheduler will not start.")
        return None

    scheduler = BackgroundScheduler()

    # Daily job: every day at 09:00
    scheduler.add_job(
        func=reminder_task,
        trigger=CronTrigger(hour=9, minute=0),
        id="daily_reminder",
        replace_existing=True,
        max_instances=1,
    )
    logger.info("Scheduled job: daily_reminder at 09:00")

    # Optional test job — helpful during development. Set skip_test_job=False to enable.
    if not skip_test_job:
        scheduler.add_job(
            func=reminder_task,
            trigger=IntervalTrigger(seconds=30),
            id="test_every_30s",
            replace_existing=True,
            max_instances=1,
        )
        logger.info("Scheduled test job: test_every_30s every 30s")

    scheduler.start()
    logger.info("BackgroundScheduler started")
    return scheduler
