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
    
    def get_average_scores(self):
        return self.reviews.aggregate(
            avg_story=models.Avg('storyline_score'),
            avg_visual=models.Avg('visual_score'),
            avg_sound=models.Avg('soundtrack_score')
        )
    
    def __str__(self):
        return self.title

class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
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
    is_approved = models.BooleanField(default=False)

    def average_score(self):
        scores = [self.storyline_score, self.visual_score, self.soundtrack_score]
        valid_scores = [s for s in scores if s is not None]
        if not valid_scores:
            return 0
        return sum(valid_scores) / len(valid_scores)

    def __str__(self):
        return f"{self.movie.title} - {self.author.username}"