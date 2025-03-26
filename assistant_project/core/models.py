from django.db import models
from django.contrib.auth.models import User  # Importing User model for user authentication

from django.db import models

# class Reminder(models.Model):
#     title = models.CharField(max_length=200)
#     description = models.TextField(blank=True, null=True)
#     due_date = models.DateField()  # Date field
#     due_time = models.TimeField(default="00:00:00")  # Time field with default value

#     def __str__(self):
#         return self.title

# from django.db import models

# class Reminder(models.Model):
#     message = models.CharField(max_length=255)
#     scheduled_time = models.DateTimeField()
    
#     def __str__(self):
#         return self.message

from django.utils import timezone
from django.db import models

class Reminder(models.Model):
    text = models.CharField(max_length=255)
    time = models.DateTimeField(default=timezone.now)  # Set default to current time





# class Reminder(models.Model):
#     title = models.CharField(max_length=200)
#     description = models.TextField(blank=True, null=True)
#     due_date = models.DateField()  # Date field
#     due_time = models.TimeField()  # Time field

#     def __str__(self):
#         return f"{self.due_date} ({self.due_time})"


# EmergencyContact model to store user emergency contact information
class EmergencyContact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Links contact to a specific user
    contact_name = models.CharField(max_length=100)  # Name of the emergency contact
    phone = models.CharField(max_length=15)  # Phone number of the emergency contact

    def __str__(self):
        return f"{self.contact_name} ({self.phone})"




# class Reminder(models.Model):
#     title = models.CharField(max_length=200)
#     description = models.TextField(blank=True, null=True)
#     due_date = models.DateTimeField()



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



from django.db import models
from django.utils import timezone  # Make sure this is imported

class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    due_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)  # ✅ Ensure this is correct

    def __str__(self):
        return self.title

    

