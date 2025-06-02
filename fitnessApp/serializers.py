from rest_framework import serializers
from .models import FitnessEntry
from django.contrib.auth.models import User

class FitnessEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = FitnessEntry
        fields = ['id', 'user', 'activity_type', 'duration_minutes', 'date_recorded', 'notes']
        read_only_fields = ['date_recorded', 'user']

