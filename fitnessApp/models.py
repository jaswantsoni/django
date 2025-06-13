from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.username

class FitnessEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='fitness_entries')
    activity_type = models.CharField(max_length=100)
    duration_minutes = models.IntegerField()
    date_recorded = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Fitness Entries"
        ordering = ['-date_recorded']

    def __str__(self):
        return f"{self.user.username}'s {self.activity_type} on {self.date_recorded.strftime('%Y-%m-%d')}"