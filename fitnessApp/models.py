from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    age = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return self.username

class FitnessEntry(models.Model):
    User = models.ForeignKey('fitnessApp.User', on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=100)
    duration_minutes = models.PositiveIntegerField()
    date_recorded = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.activity_type}"

    class Meta:
        ordering = ['-date_recorded']
