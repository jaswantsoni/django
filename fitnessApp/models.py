from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    
    def __str__(self):
        return self.username


class FitnessEntry(models.Model):
  
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='fitness_entries')

   
    ACTIVITY_CHOICES = [
        ('Running', 'Running'),
        ('Weightlifting', 'Weightlifting'),
        ('Cycling', 'Cycling'),
        ('Swimming', 'Swimming'),
        ('Yoga', 'Yoga'),
        ('Walking', 'Walking'),
        ('Other', 'Other'),
    ]
    activity_type = models.CharField(max_length=50, choices=ACTIVITY_CHOICES)

    
    duration_minutes = models.PositiveIntegerField()

   
    notes = models.TextField(blank=True, null=True)

    
    date_recorded = models.DateTimeField(auto_now_add=True)

    class Meta:
        
    
        ordering = ['-date_recorded']
      
        verbose_name_plural = "Fitness Entries"

    def __str__(self):
       
        return f"{self.user.username}'s {self.activity_type} on {self.date_recorded.strftime('%Y-%m-%d')}"



    class Meta:
        verbose_name_plural = "Fitness Entries"
        ordering = ['-date_recorded']

    def __str__(self):
        return f"{self.user.username}'s {self.activity_type} on {self.date_recorded.strftime('%Y-%m-%d')}"