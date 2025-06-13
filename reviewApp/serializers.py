from rest_framework import serializers
from .models import User, MovieReview

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class MovieReviewSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source='author.username')
    
    class Meta:
        model = MovieReview
        fields = [
            'id', 'author', 'author_username', 'movie_title', 'storyline_score', 
            'visual_score', 'soundtrack_score',  'created_at'
        ]
        read_only_fields = ['author', 'created_at']
