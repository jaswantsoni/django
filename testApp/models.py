from django.db import models
from django.contrib.auth.models import User

class FitnessEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=100)
    duration_minutes = models.IntegerField()
    date_recorded = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.activity_type} on {self.date_recorded.strftime('%Y-%m-%d')}"

    class Meta:
        ordering = ['-date_recorded']