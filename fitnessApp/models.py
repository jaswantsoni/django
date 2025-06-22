from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import date, timedelta
from .hooks import call_hooks



class User(AbstractUser):
    streak_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.username

class FitnessEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='fitness_entries')
    title = models.CharField(max_length=100)
    duration = models.IntegerField(help_text="Duration in minutes")
    date = models.DateField(default=date.today)

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

    duration = models.PositiveIntegerField()
    notes = models.TextField(blank=True, null=True)
    date_recorded = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Fitness Entries"
        ordering = ['-date_recorded']

    def __str__(self):
        return f"{self.user.username}'s {self.activity_type} on {self.date_recorded.strftime('%Y-%m-%d')}"

    def save(self, *args, **kwargs):
        from .hooks import call_hooks
        call_hooks('before_save_fitnessentry', self)

        # Auto-fill duration_minutes from duration if not provided
        if not self.duration:
            self.duration = self.duration

        # Streak logic inside model save
        today = date.today()
        yesterday = today - timedelta(days=1)

        if not self.pk:  # Only apply on create, not update
            last_entry = FitnessEntry.objects.filter(user=self.user).order_by('-date').first()
            if last_entry:
                if last_entry.date == today:
                    pass  # already logged today
                elif last_entry.date == yesterday:
                    self.user.streak_count += 1  # continue streak
                else:
                    self.user.streak_count = 1  # reset
            else:
                self.user.streak_count = 1  # first entry
            self.user.save()

        super().save(*args, **kwargs)
class Achievement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    date_earned = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_earned']

    def __str__(self):
        return f"{self.title} - {self.user.username}"

class BlockedIP(models.Model):
    ip_address = models.GenericIPAddressField(unique=True)
    reason = models.CharField(max_length=255, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.ip_address} ({self.reason})"
    
