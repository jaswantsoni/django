from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, FitnessEntryForm
from .models import FitnessEntry

def register_view(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'register_form': form})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user is not None:
                login(request, user)
                return redirect('home')
        else:
            return render(request, 'registration/login.html', {'login_form': form})
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'login_form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def home_view(request):
    if request.method == 'POST':
        form = FitnessEntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user
            entry.save()
            return redirect('home')
    else:
        form = FitnessEntryForm()
    entries = FitnessEntry.objects.filter(user=request.user)
    return render(request, 'registration/home.html', {
        'fitness_entry_form': form,
        'fitness_entries': entries
    })
