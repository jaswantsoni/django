from rest_framework import serializers
from .models import User, FitnessEntry, Achievement
from django.contrib.auth.password_validation import validate_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name','streak_count', 'date_joined', 'last_login']
        read_only_fields = ['id', 'date_joined', 'last_login']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2', 'first_name', 'last_name']
        extra_kwargs = {
            'first_name': {'required': False},
            'last_name': {'required': False},
            'email': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user

class FitnessEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = FitnessEntry
        fields = [
            'id', 'user', 'title', 'activity_type', 'duration_minutes',
            'notes', 'date', 'date_recorded'
        ]
        read_only_fields = ['id', 'user', 'date_recorded']

class AchievementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Achievement
        fields = ['id', 'user', 'title', 'description', 'date_earned']
        read_only_fields = ['id', 'date_earned']
