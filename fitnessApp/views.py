from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
import csv
from .models import Achievement
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.parsers import MultiPartParser, FormParser
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from rest_framework_simplejwt.tokens import RefreshToken
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.core.cache import cache
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import User, FitnessEntry, BlockedIP, Achievement
from .serializers import UserSerializer, FitnessEntrySerializer, RegisterSerializer, AchievementSerializer
from .forms import LoginForm, RegisterForm, FitnessEntryForm
from .hooks import call_hooks
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import FitnessEntry
from django.db.models import Avg, Sum


@login_required
def dashboard_view(request):
    entries = FitnessEntry.objects.filter(user=request.user)
    
    context = {
        "total_activities": entries.count(),
        "total_duration": entries.aggregate(Sum("duration"))["duration__sum"] or 0,
        "average_duration": round(entries.aggregate(Avg("duration"))["duration__avg"] or 0, 2),
        "total_calories": sum(e.calories_burned() for e in entries),
    }
    return render(request, "dashboard.html", context)


#from .utils import S3ImageUploader


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ['create', 'list']:
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [AllowAny]
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
    print("Authentication failed")
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



class HomeTemplateView(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        
        entries = FitnessEntry.objects.filter(user=self.request.user)

      
        search = self.request.GET.get('search', '')
        sort_by = self.request.GET.get('sort', 'date_desc')
        start_date = self.request.GET.get('start')
        end_date = self.request.GET.get('end')

        if search:
            entries = entries.filter(activity_type__icontains=search)

        if start_date and end_date:
            entries = entries.filter(date__range=[start_date, end_date])

        if sort_by == 'date_asc':
            entries = entries.order_by('date')
        elif sort_by == 'duration_asc':
            entries = entries.order_by('duration')
        elif sort_by == 'duration_desc':
            entries = entries.order_by('-duration')
        else:
            entries = entries.order_by('-date')

       
        paginator = Paginator(entries, 3)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context.update({
            'fitness_entries': page_obj,
            'page_obj': page_obj,
            'search': search,
            'sort_by': sort_by,
            'start_date': start_date,
            'end_date': end_date,
            'total_activities': entries.count(),
            'total_duration': sum(e.duration for e in entries),
            'streak': self.request.user.streak_count,
            'achievements': Achievement.objects.filter(user=self.request.user),

            })


       

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

 # make sure this import is correct

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
                
                send_mail(
                    'Login Alert - Fitness App',
                    'Hi {},\n\nYou have logged in successfully to your account.'.format(user.username),
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                    fail_silently=True
                )
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

# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# @parser_classes([MultiPartParser, FormParser])
# def upload_image(request):
#     if 'image' not in request.FILES:
#         return Response({'error': 'No image file provided'}, status=status.HTTP_400_BAD_REQUEST)
#     image_file = request.FILES['image']
#     folder = request.data.get('folder', 'images/')
#     uploader = S3ImageUploader()
#     result = uploader.upload_image(image_file, folder)
#     if result['success']:
#         return Response({
#             'message': 'Image uploaded successfully',
#             'url': result['url'],
#             'key': result['key'],
#             'filename': result['filename']
#         }, status=status.HTTP_201_CREATED)
#     else:
#         return Response({'error': result['error']}, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['DELETE'])
# @permission_classes([IsAuthenticated])
# def delete_image(request):
#     s3_key = request.data.get('key')
#     if not s3_key:
#         return Response({'error': 'S3 key is required'}, status=status.HTTP_400_BAD_REQUEST)
#     uploader = S3ImageUploader()
#     result = uploader.delete_image(s3_key)
#     if result['success']:
#         return Response({'message': 'Image deleted successfully'}, status=status.HTTP_200_OK)
#     else:
#         return Response({'error': result['error']}, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# @parser_classes([MultiPartParser, FormParser])
# def upload_multiple_images(request):
#     if 'images' not in request.FILES:
#         return Response({'error': 'No image files provided'}, status=status.HTTP_400_BAD_REQUEST)
#     images = request.FILES.getlist('images')
#     folder = request.data.get('folder', 'images/')
#     if len(images) > 10:
#         return Response({'error': 'Maximum 10 images allowed'}, status=status.HTTP_400_BAD_REQUEST)
#     uploader = S3ImageUploader()
#     results = []
#     errors = []
#     for image in images:
#         result = uploader.upload_image(image, folder)
#         if result['success']:
#             results.append({
#                 'filename': result['filename'],
#                 'url': result['url'],
#                 'key': result['key']
#             })
#         else:
#             errors.append({
#                 'filename': image.name,
#                 'error': result['error']
#             })
#     return Response({
#         'message': f'{len(results)} images uploaded successfully',
#         'uploaded': results,
#         'errors': errors
#     }, status=status.HTTP_201_CREATED if results else status.HTTP_400_BAD_REQUEST)
login_required
def export_fitness_csv(request):
    entries = FitnessEntry.objects.filter(user=request.user)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="fitness_data.csv"'

    writer = csv.writer(response)
    writer.writerow(['Date', 'Activity Type', 'Duration (min)', 'Notes'])

    for entry in entries:
        writer.writerow([
            entry.date_recorded.strftime('%Y-%m-%d %H:%M'),
            entry.activity_type,
            entry.duration,
            entry.notes or ''
        ])

    return response

