from django import forms
from django.contrib.auth.models import User
from .models import FitnessEntry

class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords do not match.')
        return cd['password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class FitnessEntryForm(forms.ModelForm):
    class Meta:
        model = FitnessEntry
        fields = ['activity_type', 'duration_minutes', 'notes']
        widgets = {
            'activity_type': forms.TextInput(attrs={'placeholder': 'e.g., Running, Cycling, Weightlifting'}),
            'duration_minutes': forms.NumberInput(attrs={'placeholder': 'e.g., 30, 60'}),
            'notes': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Optional notes about your workout...'}),
        }