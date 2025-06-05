from rest_framework import serializers
from .models import User, FitnessEntry
from django.contrib.auth.password_validation import validate_password


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number', 'age', 'password', 'confirm_password']

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = User.objects.create_user(**validated_data)
        return user

class FitnessEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = FitnessEntry
        fields = '__all__'

class LoginResponseSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    access = serializers.CharField()
