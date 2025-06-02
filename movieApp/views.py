from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from .models import Movie, Review, Genre
from .forms import ReviewForm

def home(request):
    movies = Movie.objects.annotate(
        avg_score=Avg('reviews__storyline_score') + 
                 Avg('reviews__visual_score') + 
                 Avg('reviews__soundtrack_score') / 3
    )
    genres = Genre.objects.all()
    
    genre_filter = request.GET.get('genre')
    if genre_filter:
        movies = movies.filter(genre__name=genre_filter)
    
    return render(request, 'home.html', {
        'movies': movies,
        'genres': genres,
        'selected_genre': genre_filter
    })

def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    reviews = movie.reviews.filter(is_approved=True)
    
    return render(request, 'movie_detail.html', {
        'movie': movie,
        'reviews': reviews
    })

@login_required
def create_review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            review = form.save(commit=False)
            review.author = request.user
            review.save()
            return redirect('movie_detail', movie_id=review.movie.id)
    else:
        form = ReviewForm()
    
    return render(request, 'create_review.html', {'form': form})

def welcome(request):
    return render(request, 'welcome.html')

def filter_movies(request):
    genre_id = request.GET.get('genre')
    if genre_id:
        movies = Movie.objects.filter(genre__id=genre_id)
    else:
        movies = Movie.objects.all()
    genres = Genre.objects.all()
    return render(request, 'home.html', {
        'movies': movies,
        'genres': genres,
        'selected_genre': int(genre_id) if genre_id else None
    })