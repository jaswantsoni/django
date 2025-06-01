from rest_framework import serializers
from .models import User, Skill, SkillSession, Rating

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id', 'name']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'is_verified', 'bio', 'skills_can_teach', 'skills_want_to_learn']

class SkillSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SkillSession
        fields = '__all__'
        read_only_fields = ['created_at']

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'
