from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Q
from .models import Movie, Review, Genre
from .forms import ReviewForm
from .serializer import MovieSerializer, ReviewSerializer, GenreSerializer
from rest_framework import viewsets, permissions, filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle


def welcome(request):
    return render(request, 'welcome.html')

def movie_list(request):
    movies = Movie.objects.all()
    return render(request, 'movie_list.html', {'movies': movies})
    

@login_required
def create_review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            review = form.save(commit=False)
            review.author = request.user
            review.save()
            return redirect('movie:movie_list')
    else:
        initial_data = {}
        movie_id = request.GET.get('movie')
        if movie_id:
            initial_data['movie'] = movie_id
        form = ReviewForm(initial=initial_data)
    
    return render(request, 'create_review.html', {'form': form})


def movie_detail(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    return render(request, 'movie_detail.html', {'movie': movie})


from rest_framework import viewsets
from .models import Movie, Review
from .serializer import MovieSerializer, ReviewSerializer

class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)