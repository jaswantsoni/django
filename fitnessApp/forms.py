from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, FitnessEntry

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email',  'password1', 'password2']

class FitnessEntryForm(forms.ModelForm):
    class Meta:
        model = FitnessEntry
        fields = ['activity_type', 'duration_minutes', 'notes']