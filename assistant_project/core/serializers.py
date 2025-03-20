from datetime import timezone
from rest_framework import serializers
from .models import Reminder , EmergencyContact

from rest_framework import serializers
from .models import Reminder  # Ensure the model is correctly imported

class ReminderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reminder  # Link the Reminder model
        fields = '__all__'  # Include all fields from the model

  

class EmergencyContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmergencyContact  # The model the serializer is for
        fields = '__all__'  # Include all fields from the EmergencyContact model




# class ReminderSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Reminder  # Ensure this matches the Reminder model name
#         fields = '__all__'  # Ensure all fields are included





