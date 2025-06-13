from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import F
from .forms import MovieReviewForm
from .models import MovieReview

def is_verified(user):
    return user.is_authenticated and user.is_verified

@login_required
@user_passes_test(is_verified)
def submit_review(request):
    if request.method == 'POST':
        form = MovieReviewForm(request.POST, request.FILES)
        if form.is_valid():
            review = form.save(commit=False)
            review.author = request.user
            review.save()
            return redirect('review_list')
    else:
        form = MovieReviewForm()
    return render(request, 'reviewApp/submit_review.html', {'form': form})

def review_list(request):
    reviews = MovieReview.objects.annotate(
        average_score=(F('storyline_score') + F('visual_score') + F('soundtrack_score')) / 3
    ).order_by('-created_at')
    return render(request, 'reviewApp/review_list.html', {'reviews': reviews})


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