from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets, permissions, filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from .models import User, Post, Comment
from .serializers import UserSerializer, PostSerializer, CommentSerializer

@login_required
def dashboard(request):
    # Only logged in users can access this
    if request.user.is_authenticated:
        return render(request, 'pages/page1.html')

def home(request):
    return HttpResponse("Hello, world. You're at the testApp index.")

def root(request):
    return render(request, 'registration/login.html')

# API Views
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = StandardResultsSetPagination
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering_fields = ['username', 'joined_at']
    
    def perform_create(self, serializer):
        serializer.save()

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = StandardResultsSetPagination
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'content', 'author__username']
    ordering_fields = ['created_at', 'title']
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    pagination_class = StandardResultsSetPagination
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['content', 'author__username', 'post__title']
    ordering_fields = ['created_at']
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    
    def get_queryset(self):
        """
        Optionally restricts the returned comments to a given post,
        by filtering against a `post_id` query parameter in the URL.
        """
        queryset = Comment.objects.all()
        post_id = self.request.query_params.get('post_id')
        if post_id is not None:
            queryset = queryset.filter(post__id=post_id)
        return queryset