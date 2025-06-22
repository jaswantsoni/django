from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from rest_framework_simplejwt.tokens import RefreshToken
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, FitnessEntry, BlockedIP
from .serializers import UserSerializer, FitnessEntrySerializer, RegisterSerializer, AchievementSerializer
from .forms import LoginForm, RegisterForm, FitnessEntryForm
from django.core.paginator import Paginator
from .hooks import call_hooks

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
    permission_classes = [IsAuthenticated]

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
    user = authenticate(username=username, password=password)
    if user is not None:
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)
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


class HomeTemplateView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        entries = FitnessEntry.objects.filter(user=self.request.user).order_by('-date_recorded')
        
        paginator = Paginator(entries, 5)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        # 🟢 ADD THESE THREE LINES:
        context['fitness_entries'] = page_obj
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


class LoginTemplateView(TemplateView):
    template_name = 'login.html'

    def get_context_data(self, **kwargs):
        return {'login_form': LoginForm()}

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request, **form.cleaned_data)
            if user is not None:
                django_login(request, user)
                messages.success(request, "Welcome back!")
                return redirect('home')
            messages.error(request, "Invalid credentials.")
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
    

# IP Block APIs
@api_view(['POST'])
@permission_classes([IsAdminUser])
def block_ip(request):
    ip = request.data.get('ip_address')
    reason = request.data.get('reason', '')
    if not ip:
        return Response({'error': 'IP required'}, status=400)
    from django.core.cache import cache
    blocked_ip, created = BlockedIP.objects.update_or_create(ip_address=ip, defaults={'reason': reason})
    cache.delete(f'blocked_ip_{ip}')
    return Response({'message': f'Blocked {ip}'})

@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def unblock_ip(request, ip_address):
    try:
        BlockedIP.objects.get(ip_address=ip_address).delete()
        from django.core.cache import cache
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
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Achievement.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
