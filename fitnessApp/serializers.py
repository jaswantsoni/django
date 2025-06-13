from rest_framework import serializers
from .models import User, FitnessEntry

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone_number', 'age']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number', 'age', 'password']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class FitnessEntrySerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = FitnessEntry
        fields = ['id', 'user', 'activity_type', 'duration_minutes', 'date_recorded', 'notes']