
from django.contrib import admin
from .models import Reminder, EmergencyContact

admin.site.register(Reminder)
admin.site.register(EmergencyContact)
