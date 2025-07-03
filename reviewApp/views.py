from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import MovieReviewForm
from .models import MovieReview
from .decorators import verified_required
from django.contrib import messages #for message
from django.shortcuts import get_object_or_404


# def is_verified(user):
#     return user.is_authenticated and user.is_verified


def home(request):
    return render(request, 'reviewApp/home.html')

@login_required
def index(request):
    return render(request, 'reviewApp/index.html')

@login_required
#@user_passes_test(is_verified, login_url='/not-verified/')
@verified_required
def submit_review(request):
    if request.method == 'POST':
        form = MovieReviewForm(request.POST, request.FILES)
        if form.is_valid():
            review = form.save(commit=False)
            review.author = request.user
            review.save()

            #for signal - pop up mssg
            messages.success(request, 'Your review has been submitted!*')

            return redirect('review_list')
    else:
        form = MovieReviewForm()
    return render(request, 'reviewApp/submit_review.html', {'form': form})

@login_required
def review_list(request):
    from django.db.models import F, Avg
    movies = (
        MovieReview.objects
        .values('movie_title')
        .annotate(avg_score=Avg((F('storyline_score') + F('visual_score') + F('soundtrack_score')) / 3))
        .order_by('movie_title')
    )
    return render(request, 'reviewApp/review_list.html', {'movies': movies})

#shows all rvws for a particular movie
@login_required
def movie_reviews(request, movie_title):
    reviews = MovieReview.objects.filter(movie_title=movie_title)
    return render(request, 'reviewApp/movie_review.html', {
        'movie_title': movie_title,
        'reviews': reviews
    })

#my own rvws
@login_required
def user_reviews(request):
    reviews = MovieReview.objects.filter(author=request.user)
    return render(request, 'reviewApp/user_review.html', {'reviews': reviews})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_verified = True  #optionally: auto-verifying on signup (remember)
            user.save()
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

from django.contrib.auth import logout as auth_logout

def logout_view(request):
    auth_logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('home')

#from django.http import HttpResponse

def not_verified(request):
    return render(request, 'reviewApp/not_verified.html')


from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import User, MovieReview
from .serializers import UserSerializer, MovieReviewSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class MovieReviewViewSet(viewsets.ModelViewSet):
    queryset = MovieReview.objects.all()
    serializer_class = MovieReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)



##for sync and async api (13/6/25)
def sync_view(request):
    return "this is an sync api"

async def async_view(request):
    return "this is an async view"




###########################################################################
##FOR IP BLOCKING

from .models import BlockedIP
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework import status

# IP Blocking API endpoints
@api_view(['POST'])
@permission_classes([IsAdminUser])
def block_ip(request):
    """Block an IP address"""
    ip_address = request.data.get('ip_address')
    reason = request.data.get('reason', '')
   
    if not ip_address:
        return Response({'error': 'IP address is required'}, status=status.HTTP_400_BAD_REQUEST)
   
    # Create or update the blocked IP
    blocked_ip, created = BlockedIP.objects.update_or_create(
        ip_address=ip_address,
        defaults={'reason': reason}
    )
   
    # Clear cache for this IP
    from django.core.cache import cache
    cache.delete(f'blocked_ip_{ip_address}')
   
    if created:
        return Response({'message': f'IP {ip_address} has been blocked'}, status=status.HTTP_201_CREATED)
    else:
        return Response({'message': f'IP {ip_address} block has been updated'}, status=status.HTTP_200_OK)
 
@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def unblock_ip(request, ip_address):
    """Unblock an IP address"""
    try:
        blocked_ip = BlockedIP.objects.get(ip_address=ip_address)
        blocked_ip.delete()
       
        # Clear cache for this IP
        from django.core.cache import cache
        cache.delete(f'blocked_ip_{ip_address}')
       
        return Response({'message': f'IP {ip_address} has been unblocked'}, status=status.HTTP_200_OK)
    except BlockedIP.DoesNotExist:
        return Response({'error': f'IP {ip_address} is not blocked'}, status=status.HTTP_404_NOT_FOUND)
 
@api_view(['GET'])
@permission_classes([IsAdminUser])
def list_blocked_ips(request):
    """List all blocked IPs"""
    blocked_ips = BlockedIP.objects.all().order_by('ip_address')
    data = [{'ip_address': ip.ip_address, 'reason': ip.reason, 'date_added': ip.date_added} for ip in blocked_ips]
    return Response(data)


#####for aws integration
# Image Upload API endpoints

 
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from .utils import S3ImageUploader


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def upload_image(request):
    """Upload image to AWS S3"""
    if 'image' not in request.FILES:
        return Response({'error': 'No image file provided'}, status=status.HTTP_400_BAD_REQUEST)
   
    image_file = request.FILES['image']
    folder = request.data.get('folder', 'images/')
   
    # Initialize S3 uploader
    uploader = S3ImageUploader()
   
    # Upload image
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
    """Delete image from AWS S3"""
    s3_key = request.data.get('key')
   
    if not s3_key:
        return Response({'error': 'S3 key is required'}, status=status.HTTP_400_BAD_REQUEST)
   
    # Initialize S3 uploader
    uploader = S3ImageUploader()
   
    # Delete image
    result = uploader.delete_image(s3_key)
   
    if result['success']:
        return Response({'message': 'Image deleted successfully'}, status=status.HTTP_200_OK)
    else:
        return Response({'error': result['error']}, status=status.HTTP_400_BAD_REQUEST)
 
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def upload_multiple_images(request):
    """Upload multiple images to AWS S3"""
    if 'images' not in request.FILES:
        return Response({'error': 'No image files provided'}, status=status.HTTP_400_BAD_REQUEST)
   
    images = request.FILES.getlist('images')
    folder = request.data.get('folder', 'images/')
   
    if len(images) > 10:  # Limit to 10 images
        return Response({'error': 'Maximum 10 images allowed'}, status=status.HTTP_400_BAD_REQUEST)
   
    # Initialize S3 uploader
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
