from django.db import models
from django.contrib.auth.models import AbstractUser

# Custom User model
class User(AbstractUser):
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

class Genre(models.Model):
    name=models.CharField(max_length=100)

    def __str__(self):
        return self.name
# Movie model
class Movie(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# Review model
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
    comment = models.TextField()
    visual_score=models.IntegerField()
    soundtrack_score=models.IntegerField()
    storyline_score=models.IntegerField()
    breakdown_pdf=models.FileField(upload_to='breakdowns/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} on {self.movie.title}"
    
    def average_score(self):
        return round((self.storyline_score + self.visual_score + self.soundtrack_score) / 3, 2)
