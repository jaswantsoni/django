# JobPortalApp/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, JobPost, Application


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "Email"}
        ),
    )
    is_recruiter = forms.BooleanField(
        required=False,
        label="Register as Recruiter",
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
    )

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2", "is_recruiter"]


class JobPostForm(forms.ModelForm):
    class Meta:
        model = JobPost
        fields = ["title", "description"]


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ["cover_letter"]
