
from .scheduler import start_scheduler
from django.apps import AppConfig
from .accessibility import setup_keyboard_shortcuts
from django.db import models
# from django.contrib.auth.models import User 

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        # Import inside ready() to avoid early import issues
        from django.contrib.auth.models import User


# class CoreConfig(AppConfig):
#     default_auto_field = 'django.db.models.BigAutoField'
#     name = 'core'

#     def ready(self):
#         setup_keyboard_shortcuts()

 # Problem: This is too early


# class CoreConfig(AppConfig):
#     default_auto_field = 'django.db.models.BigAutoField'
#     name = 'core'

#     def ready(self):
#         # Import models, tasks, or signals *only* within the ready() method
#         from django.contrib.auth.models import User
#         from .scheduler import start_scheduler
#         from .accessibility import setup_keyboard_shortcuts

#         # Call your setup functions here
#         setup_keyboard_shortcuts()
#         start_scheduler()

from django.apps import AppConfig

class coreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        from .tasks import scheduler  # Import scheduler to ensure it starts
