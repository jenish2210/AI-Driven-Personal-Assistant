from core.models import Reminder, EmergencyContact
from django.contrib.auth.models import User

# Create a sample user
user = User.objects.create_user(username='testuser', password='password123')

# Create a reminder for the user
reminder = Reminder.objects.create(user=user, title="Take medication", time="2025-01-08 09:00:00")

# Create an emergency contact for the user
emergency_contact = EmergencyContact.objects.create(user=user, contact_name="John Doe", phone="+1234567890")

# Print to verify the created objects
print(reminder)
print(emergency_contact)
