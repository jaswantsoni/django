from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from django.contrib.auth import authenticate, login as django_login
from django.contrib.auth.models import update_last_login
from rest_framework_simplejwt.tokens import RefreshToken
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth import logout as django_logout
from .models import User, FitnessEntry
from .serializers import UserSerializer, FitnessEntrySerializer, RegisterSerializer
from .forms import LoginForm, RegisterForm, FitnessEntryForm


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [AllowAny] 
        elif self.action == 'list':
            self.permission_classes = [IsAdminUser]  
        elif self.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAuthenticated] 
        else:
            self.permission_classes = [IsAuthenticated]  
        return super().get_permissions()

    def get_queryset(self):
        
        if self.request.user.is_staff:
            return User.objects.all()
        return User.objects.filter(id=self.request.user.id)


class FitnessEntryViewSet(viewsets.ModelViewSet):
   
    queryset = FitnessEntry.objects.all()
    serializer_class = FitnessEntrySerializer
    permission_classes = [IsAuthenticated] 

    def get_queryset(self):
       
        return FitnessEntry.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
       
        serializer.save(user=self.request.user)




class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save() 
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny]) 
def login_view(request):
    username = request.data.get("username")
    password = request.data.get("password")

    user = authenticate(username=username, password=password)
    if user is not None:
        refresh = RefreshToken.for_user(user)
        update_last_login(None, user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)
    return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([IsAuthenticated]) 
def logout_view(request):
    try:
        refresh_token = request.data.get("refresh")
        token = RefreshToken(refresh_token)
        token.blacklist() 
        django_logout(request) 
        return Response({"message": "Logged out successfully."}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": "Invalid refresh token or token already blacklisted."}, status=status.HTTP_400_BAD_REQUEST)





class HomeTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'home.html'
    login_url = '/login/' 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Retrieve all fitness entries for the current authenticated user
        context['fitness_entries'] = FitnessEntry.objects.filter(user=self.request.user)
        return context



class AddFitnessEntryTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'add-activity.html'
    login_url = '/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
       
        context['fitness_entry_form'] = FitnessEntryForm()
        return context

    def post(self, request, *args, **kwargs):

        form = FitnessEntryForm(request.POST)
        if form.is_valid():
            fitness_entry = form.save(commit=False)
            fitness_entry.user = request.user
            fitness_entry.save()
            messages.success(request, "Fitness activity logged successfully!")
            return redirect('home') 
        else:
            messages.error(request, "Error logging activity. Please check your input.")
           
            return render(request, self.template_name, {
                'fitness_entry_form': form,
            })



class LoginTemplateView(TemplateView):
    template_name = 'login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['login_form'] = LoginForm() 
        return context

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                django_login(request, user) 
                messages.success(request, f"Welcome back, {user.username}!")
                return redirect('home') 
            else:
                messages.error(request, "Invalid username or password.")
        
        return render(request, self.template_name, {'login_form': form})


class RegisterTemplateView(TemplateView):
    template_name = 'register.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['register_form'] = RegisterForm() 
        return context

    def post(self, request, *args, **kwargs):
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save() 
            messages.success(request, "Registration successful! Please log in.")
            return redirect('login') 
        else:
            messages.error(request, "Error during registration. Please correct the errors below.")
        
        return render(request, self.template_name, {'register_form': form})


class LogoutTemplateView(TemplateView):
    def get(self, request, *args, **kwargs):
        django_logout(request) 
        messages.info(request, "You have been logged out.")
        return redirect('login') 
