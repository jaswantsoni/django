from rest_framework import serializers
from .models import Genre, Movie, Review
from django.contrib.auth import get_user_model

User = get_user_model()

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']
        read_only_fields = ['id']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
        read_only_fields = ['id']

class MovieSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(read_only=True)
    genre_id = serializers.PrimaryKeyRelatedField(
        queryset=Genre.objects.all(),
        source='genre',
        write_only=True
    )
    
    get_average_scores = serializers.SerializerMethodField()
    
    class Meta:
        model = Movie
        fields = [
            'id', 'title', 'genre', 'genre_id', 'created_at',
            'average_storyline', 'average_visual', 'average_soundtrack'
        ]
        read_only_fields = ['id', 'created_at']

    def get_average_storyline(self, obj):
        return obj.get_average_storyline()

    def get_average_visual(self, obj):
        return obj.get_average_visual()

    def get_average_soundtrack(self, obj):
        return obj.get_average_soundtrack()

class ReviewSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    movie = serializers.PrimaryKeyRelatedField(queryset=Movie.objects.all())
    average_score = serializers.SerializerMethodField()
    breakdown_pdf_url = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = [
            'id', 'movie', 'author', 'comment',
            'storyline_score', 'visual_score', 'soundtrack_score',
            'breakdown_pdf', 'breakdown_pdf_url', 'average_score',
            'is_approved', 'created_at'
        ]
        read_only_fields = ['id', 'author', 'created_at', 'average_score']
        extra_kwargs = {
            'storyline_score': {'min_value': 1, 'max_value': 10},
            'visual_score': {'min_value': 1, 'max_value': 10},
            'soundtrack_score': {'min_value': 1, 'max_value': 10},
        }

    def get_average_score(self, obj):
        return obj.average_score()

    def get_breakdown_pdf_url(self, obj):
        if obj.breakdown_pdf:
            return self.context['request'].build_absolute_uri(obj.breakdown_pdf.url)
        return None

    def create(self, validated_data):
        # Automatically set the author to the current user
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)

class MovieDetailSerializer(MovieSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    
    class Meta(MovieSerializer.Meta):
        fields = MovieSerializer.Meta.fields + ['reviews']
        