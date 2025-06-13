from django import forms
from .models import MovieReview

class MovieReviewForm(forms.ModelForm):
    class Meta:
        model = MovieReview
        fields = [
            'movie_title', 'genre', 'storyline_score', 
            'visual_score', 'soundtrack_score', 
            'review_text', 'pdf_upload'
        ]
