import time
import logging
from django.core.management.base import BaseCommand

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = "Run background scheduler (should be run as a separate service in production)"

    def handle(self, *args, **options):
        try:
            from core.scheduler import start_scheduler
        except Exception as e:
            self.stderr.write(f"Failed to import start_scheduler: {e}\n")
            logger.exception("Failed to import start_scheduler")
            return

        sched = start_scheduler(skip_test_job=True)
        if sched is None:
            self.stderr.write("Scheduler did not start. (apscheduler missing?)\n")
            return

        self.stdout.write("Scheduler started. Keeping process alive...\n")

        try:
            while True:
                time.sleep(60)
        except KeyboardInterrupt:
            self.stdout.write("Stopping scheduler...\n")
            try:
                sched.shutdown()
            except:
                pass
