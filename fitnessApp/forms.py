from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import FitnessEntry, User
from django.contrib.auth.forms import UserCreationForm

from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        label="Username",
        widget=forms.TextInput(attrs={'class': 'form-input'})
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class': 'form-input'})
    )


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


class FitnessEntryForm(forms.ModelForm):
    class Meta:
        model = FitnessEntry
        fields = ["title", "activity_type", "duration", "notes"]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'activity_type': forms.Select(attrs={'class': 'form-select'}),
            'duration': forms.NumberInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }