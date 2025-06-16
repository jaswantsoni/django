from django import forms
from .models import FitnessEntry, User


BASE_INPUT_CLASSES = "mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"

class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': BASE_INPUT_CLASSES,
            'placeholder': 'Enter your username'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': BASE_INPUT_CLASSES,
            'placeholder': 'Enter your password'
        })
    )
class RegisterForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': BASE_INPUT_CLASSES,
            'placeholder': 'Create a password'
        }),
        help_text="Your password must contain at least 8 characters."
    )
    password_confirm = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={
            'class': BASE_INPUT_CLASSES,
            'placeholder': 'Confirm your password'
        }),
        help_text="Enter the same password as above, for verification."
    )

    class Meta:
        model = User
       
        fields = ['username', 'email', 'password', 'password_confirm', 'first_name', 'last_name']
       
        widgets = {
            'username': forms.TextInput(attrs={
                'class': BASE_INPUT_CLASSES,
                'placeholder': 'Choose a username'
            }),
            'email': forms.EmailInput(attrs={
                'class': BASE_INPUT_CLASSES,
                'placeholder': 'your.email@example.com'
            }),
            'first_name': forms.TextInput(attrs={
                'class': BASE_INPUT_CLASSES,
                'placeholder': 'Optional'
            }),
            'last_name': forms.TextInput(attrs={
                'class': BASE_INPUT_CLASSES,
                'placeholder': 'Optional'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password and password_confirm and password != password_confirm:
        
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False) 
        user.set_password(self.cleaned_data["password"]) 
        if commit:
            user.save() 
        return user


class FitnessEntryForm(forms.ModelForm):
    class Meta:
        model = FitnessEntry
        
        fields = ['activity_type', 'duration_minutes', 'notes']
        widgets = {
            'activity_type': forms.Select(attrs={
                'class': BASE_INPUT_CLASSES + " appearance-none pr-8" 
            }),
            'duration_minutes': forms.NumberInput(attrs={
                'class': BASE_INPUT_CLASSES,
                'placeholder': 'e.g., 30'
            }),
            'notes': forms.Textarea(attrs={
                'class': BASE_INPUT_CLASSES + " resize-y", 
                'rows': 3,
                'placeholder': 'Any additional notes?'
            }),
        }