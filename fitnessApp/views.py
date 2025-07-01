from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.parsers import MultiPartParser, FormParser
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from rest_framework_simplejwt.tokens import RefreshToken
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.core.cache import cache
from .models import User, FitnessEntry, BlockedIP, Achievement
from .serializers import UserSerializer, FitnessEntrySerializer, RegisterSerializer, AchievementSerializer
from .forms import LoginForm, RegisterForm, FitnessEntryForm
from .hooks import call_hooks
#from .utils import S3ImageUploader
from django.contrib.auth.mixins import LoginRequiredMixin

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ['create', 'list']:
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    def get_queryset(self):
        if self.request.user.is_staff:
            return User.objects.all()
        return User.objects.filter(id=self.request.user.id)

class FitnessEntryViewSet(viewsets.ModelViewSet):
    serializer_class = FitnessEntrySerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return FitnessEntry.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        call_hooks('before_save_fitness_entry', self.request.user)
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
    print("🔍 Attempt login for:", username)
    user = authenticate(username=username, password=password)
    if user is not None:
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)
    print("❌ Authentication failed")
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([AllowAny])
def logout_view(request):
    try:
        refresh_token = request.data.get("refresh")
        token = RefreshToken(refresh_token)
        token.blacklist()
        django_logout(request)
        return Response({"message": "Logged out successfully."}, status=status.HTTP_200_OK)
    except Exception:
        return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)

from django.contrib.auth.mixins import LoginRequiredMixin


class HomeTemplateView(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        entries = FitnessEntry.objects.filter(user=self.request.user)
        context['fitness_entries'] = entries
        context['total_activities'] = entries.count()
        context['total_duration'] = sum(entry.duration for entry in entries)
        context['streak'] = self.request.user.streak_count
        return context

class AddFitnessEntryTemplateView(TemplateView):
    template_name = 'add-activity.html'

    def get_context_data(self, **kwargs):
        return {'fitness_entry_form': FitnessEntryForm()}

    def post(self, request, *args, **kwargs):
        form = FitnessEntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user
            entry.save()
            messages.success(request, "Activity logged successfully!")
            return redirect('home')
        messages.error(request, "Please correct the errors.")
        return render(request, self.template_name, {'fitness_entry_form': form})

from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login as django_login
from django.contrib import messages
from django.shortcuts import redirect, render
from .forms import LoginForm  # make sure this import is correct

class LoginTemplateView(TemplateView):
    template_name = 'login.html'

    def get(self, request, *args, **kwargs):
        form = LoginForm()
        return render(request, self.template_name, {'login_form': form})

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")

            user = authenticate(request, username=username, password=password)
            if user is not None:
                django_login(request, user)
                messages.success(request, "Welcome back!")
                return redirect('home')
            else:
                print(" Authentication failed for:", username)
                messages.error(request, "Invalid username or password.")
        else:
            print(" Form validation errors:", form.errors)
            messages.error(request, "Form validation failed.")

        # Make sure this return is outside the if-blocks
        return render(request, self.template_name, {'login_form': form})



class RegisterTemplateView(TemplateView):
    template_name = 'register.html'

    def get_context_data(self, **kwargs):
        return {'register_form': RegisterForm()}

    def post(self, request, *args, **kwargs):
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registered successfully!")
            return redirect('login')
        messages.error(request, "Check the form for errors.")
        return render(request, self.template_name, {'register_form': form})

class LogoutTemplateView(TemplateView):
    def get(self, request, *args, **kwargs):
        django_logout(request)
        messages.info(request, "Logged out.")
        return redirect('login')

@api_view(['POST'])
@permission_classes([IsAdminUser])
def block_ip(request):
    ip = request.data.get('ip_address')
    reason = request.data.get('reason', '')
    if not ip:
        return Response({'error': 'IP required'}, status=400)
    blocked_ip, created = BlockedIP.objects.update_or_create(ip_address=ip, defaults={'reason': reason})
    cache.delete(f'blocked_ip_{ip}')
    return Response({'message': f'Blocked {ip}'})

@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def unblock_ip(request, ip_address):
    try:
        BlockedIP.objects.get(ip_address=ip_address).delete()
        cache.delete(f'blocked_ip_{ip_address}')
        return Response({'message': f'Unblocked {ip_address}'})
    except BlockedIP.DoesNotExist:
        return Response({'error': 'Not found'}, status=404)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def list_blocked_ips(request):
    blocked_ips = BlockedIP.objects.all()
    return Response([
        {'ip_address': ip.ip_address, 'reason': ip.reason, 'date_added': ip.date_added}
        for ip in blocked_ips
    ])

class AchievementViewSet(viewsets.ModelViewSet):
    serializer_class = AchievementSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Achievement.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
""""
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def upload_image(request):
    if 'image' not in request.FILES:
        return Response({'error': 'No image file provided'}, status=status.HTTP_400_BAD_REQUEST)
    image_file = request.FILES['image']
    folder = request.data.get('folder', 'images/')
    uploader = S3ImageUploader()
    result = uploader.upload_image(image_file, folder)
    if result['success']:
        return Response({
            'message': 'Image uploaded successfully',
            'url': result['url'],
            'key': result['key'],
            'filename': result['filename']
        }, status=status.HTTP_201_CREATED)
    else:
        return Response({'error': result['error']}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_image(request):
    s3_key = request.data.get('key')
    if not s3_key:
        return Response({'error': 'S3 key is required'}, status=status.HTTP_400_BAD_REQUEST)
    uploader = S3ImageUploader()
    result = uploader.delete_image(s3_key)
    if result['success']:
        return Response({'message': 'Image deleted successfully'}, status=status.HTTP_200_OK)
    else:
        return Response({'error': result['error']}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def upload_multiple_images(request):
    if 'images' not in request.FILES:
        return Response({'error': 'No image files provided'}, status=status.HTTP_400_BAD_REQUEST)
    images = request.FILES.getlist('images')
    folder = request.data.get('folder', 'images/')
    if len(images) > 10:
        return Response({'error': 'Maximum 10 images allowed'}, status=status.HTTP_400_BAD_REQUEST)
    uploader = S3ImageUploader()
    results = []
    errors = []
    for image in images:
        result = uploader.upload_image(image, folder)
        if result['success']:
            results.append({
                'filename': result['filename'],
                'url': result['url'],
                'key': result['key']
            })
        else:
            errors.append({
                'filename': image.name,
                'error': result['error']
            })
    return Response({
        'message': f'{len(results)} images uploaded successfully',
        'uploaded': results,
        'errors': errors
    }, status=status.HTTP_201_CREATED if results else status.HTTP_400_BAD_REQUEST)
"""