from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ContactForm

def home(request):
    return render(request, 'pages/home.html')

def login(request):
    return render(request, 'registration/login.html')

def about(request):
    return render(request, 'pages/about.html')

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Thank you for your message! We will get back to you soon.')
            return redirect('contact')
    else:
        form = ContactForm()
    return render(request, 'pages/contact.html', {'form': form})

@login_required
def dashboard(request):
    if request.user.is_authenticated:
        return render(request, 'pages/dashboard.html')

def root(request):
    return render(request, 'pages/page1.html')

