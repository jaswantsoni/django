from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = [
            'movie', 'comment', 
            'storyline_score', 'visual_score', 'soundtrack_score',
            'breakdown_pdf'
        ]
        widgets = {
            'storyline_score': forms.NumberInput(attrs={'min': 1, 'max': 10}),
            'visual_score': forms.NumberInput(attrs={'min': 1, 'max': 10}),
            'soundtrack_score': forms.NumberInput(attrs={'min': 1, 'max': 10}),
            'comment': forms.Textarea(attrs={'rows': 4}),
        }