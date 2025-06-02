from rest_framework import serializers
from .models import User, Movie, Review, Genre
from django.contrib.auth.password_validation import validate_password

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

# Post Serializer
class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['genre', 'description', 'title', 'content', 'created_at']

# Comment Serializer
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['user', 'movie', 'comment', 'visual_score', 'storyline_score', 'soundtrack_score', 'breakdown_pdf', 'created_at']
