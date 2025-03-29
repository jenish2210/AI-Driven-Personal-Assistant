from django.db import models
from django.contrib.auth.models import User  # Importing User model for user authentication

from django.utils import timezone

class Reminder(models.Model):
    title = models.CharField(max_length=255)  # Ensure this line exists
    description = models.TextField()
    due_date = models.DateTimeField()









# EmergencyContact model to store user emergency contact information
class EmergencyContact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Links contact to a specific user
    contact_name = models.CharField(max_length=100)  # Name of the emergency contact
    phone = models.CharField(max_length=15)  # Phone number of the emergency contact

    def __str__(self):
        return f"{self.contact_name} ({self.phone})"



def get_active_users():
    from django.contrib.auth.models import User
    return User.objects.filter(is_active=True)




from django.db import models

class ChatHistory(models.Model):
    user_message = models.TextField()
    bot_response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"User: {self.user_message} | Bot: {self.bot_response}"



class Task(models.Model):
    title = models.CharField(max_length=255)
    priority = models.IntegerField(default=1)
    completed = models.BooleanField(default=False)
    due_date = models.DateTimeField(null=True, blank=True)  # Ensure this is here
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title






    

