from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Movie(models.Model):
    title = models.CharField(max_length=200)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def average_storyline(self):
        return self.reviews.aggregate(models.Avg('storyline_score'))['storyline_score__avg']
    
    def average_visual(self):
        return self.reviews.aggregate(models.Avg('visual_score'))['visual_score__avg']
    
    def average_soundtrack(self):
        return self.reviews.aggregate(models.Avg('soundtrack_score'))['soundtrack_score__avg']
    
    def __str__(self):
        return self.title

class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='movie_reviews')
    comment = models.TextField()
    storyline_score = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    visual_score = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    soundtrack_score = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    breakdown_pdf = models.FileField(upload_to='breakdowns/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)  # Admin must approve reviews

    def average_score(self):
        return (self.storyline_score + self.visual_score + self.soundtrack_score) / 3

    def __str__(self):
        return f"Review for {self.movie.title} by {self.author.username}"