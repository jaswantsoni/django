from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    # Only logged in users can access this
    if request.user.is_authenticated:
        return render(request, 'pages/page1.html')


def home(request):
    return HttpResponse("Hello, world. You're at the testApp index.")

# Create your views here.

def root(request):
    return render(request, 'pages/page1.html')

def login(request):
    return render(request, 'registration/login.html')

def signup(request):
    return render(request, 'pages/signup.html')
