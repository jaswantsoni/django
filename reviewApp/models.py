from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    joined_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.username

GENRE_CHOICES = [
    ('action', 'Action'),
    ('drama', 'Drama'),
    ('comedy', 'Comedy'),
    ('horror', 'Horror'),
    ('sci-fi', 'Sci-Fi'),
]

class MovieReview(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='movie_reviews')
    movie_title = models.CharField(max_length=200)
    genre = models.CharField(max_length=50, choices=GENRE_CHOICES)
    storyline_score = models.IntegerField()
    visual_score = models.IntegerField()
    soundtrack_score = models.IntegerField()
    review_text = models.TextField()
    pdf_upload = models.FileField(upload_to='uploads/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.movie_title


## async topic
