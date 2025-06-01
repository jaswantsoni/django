from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    # Only logged in users can access this
    if request.user.is_authenticated:
        return render(request, 'templates\registration\login.html')
    
def welcome_page(request):
    return render(request, 'pages/firstpage.html')


def home(request):
    return HttpResponse("Hello, world. You're at the testApp index.")
# Create your views here.

def root(request):
    return render(request, 'pages/page1.html')

