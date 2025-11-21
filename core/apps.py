# core/apps.py
import logging
import sys
from django.apps import AppConfig

logger = logging.getLogger(__name__)

class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core"  # make sure this matches the package name and INSTALLED_APPS entry

    def ready(self):
        """
        Called when Django has finished loading apps.
        - Do lazy imports here to avoid import-time side effects.
        - Avoid starting long-running threads in the web process if possible.
        """
        # Commands during which we should NOT start the scheduler or run shortcut setup
        skip_commands = {
            "makemigrations",
            "migrate",
            "collectstatic",
            "check",
            "test",
            "shell",
            "shell_plus",
        }
        # If any of those commands are on argv, skip starting background services here.
        if any(cmd in sys.argv for cmd in skip_commands):
            logger.info("CoreConfig.ready(): skipping startup tasks for command: %s", sys.argv)
            return

        # Safe/lazy imports with graceful handling
        try:
            # accessibility setup (keyboard shortcuts); optional
            try:
                from .accessibility import setup_keyboard_shortcuts
            except Exception as e:
                setup_keyboard_shortcuts = None
                logger.debug("setup_keyboard_shortcuts import failed (will skip): %s", e)

            # scheduler start — imported lazily so missing deps won't crash app import
            try:
                from .scheduler import start_scheduler
            except Exception as e:
                start_scheduler = None
                logger.debug("start_scheduler import failed (will skip): %s", e)

            # optionally set up keyboard shortcuts (non-blocking)
            if setup_keyboard_shortcuts:
                try:
                    setup_keyboard_shortcuts()
                    logger.info("Accessibility shortcuts set up.")
                except Exception:
                    logger.exception("Error while setting up keyboard shortcuts; continuing.")

            # Start scheduler only if available
            if start_scheduler:
                try:
                    # In production prefer running scheduler as separate process.
                    # If you must run here, keep skip_test_job=True to avoid noisy test jobs.
                    start_scheduler(skip_test_job=True)
                    logger.info("Scheduler started from CoreConfig.ready()")
                except Exception:
                    logger.exception("Failed to start scheduler; continuing without it.")
        except Exception:
            # Catch anything unexpected to avoid blocking app startup
            logger.exception("Unexpected error in CoreConfig.ready(); continuing.")
