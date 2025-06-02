from django import forms
from django.contrib.auth.models import User
from .models import Review
#for login and model forms

class UserRegistration(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput)
    password2=forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model=User
        firlds=['Username','email','password']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['storyline_score', 'visual_score', 'soundtrack_score', 'comment', 'pdf']

        widgets = {
            'storyline_score': forms.NumberInput(attrs={'min': 1, 'max': 10, 'class': 'form-control'}),
            'visual_score': forms.NumberInput(attrs={'min': 1, 'max': 10, 'class': 'form-control'}),
            'soundtrack_score': forms.NumberInput(attrs={'min': 1, 'max': 10, 'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'pdf': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
