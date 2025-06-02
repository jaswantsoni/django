# --- testApp/views.py ---
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, FitnessEntryForm
from .models import FitnessEntry

def register_request(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = UserRegisterForm()
    # <--- CHANGE TEMPLATE NAMES HERE:
    return render(request=request, template_name="registration/register.html", context={"register_form": form})

def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("home")
            else:
                form.add_error(None, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    # <--- CHANGE TEMPLATE NAMES HERE:
    return render(request=request, template_name="registration/login.html", context={"login_form": form})

@login_required
def logout_request(request):
    logout(request)
    return redirect("login")

@login_required
def home_view(request):
    if request.method == "POST":
        form = FitnessEntryForm(request.POST)
        if form.is_valid():
            fitness_entry = form.save(commit=False)
            fitness_entry.user = request.user
            fitness_entry.save()
            return redirect("home")
    else:
        form = FitnessEntryForm()

    fitness_entries = FitnessEntry.objects.filter(user=request.user)

    # <--- CHANGE TEMPLATE NAMES HERE:
    return render(request=request, template_name="registration/home.html", context={
        "fitness_entry_form": form,
        "fitness_entries": fitness_entries
    })