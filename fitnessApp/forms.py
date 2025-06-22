from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import FitnessEntry, User
from django.contrib.auth.forms import UserCreationForm

class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Password'}))


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