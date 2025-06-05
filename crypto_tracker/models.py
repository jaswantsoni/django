from django.db import models
from django.conf import settings
from django.db.models import Count
from django.contrib.auth.models import User
from django.utils import timezone

class WatchEntry(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='watch_entries')
    coin_symbol = models.CharField(max_length=10)
    personal_note = models.TextField(blank=True)
    image = models.ImageField(upload_to='market_patterns/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Watch Entries'
        unique_together = ['user', 'coin_symbol']

    def __str__(self):
        return f"{self.user.username} - {self.coin_symbol}"

    @classmethod
    def get_coin_popularity(cls):
        return cls.objects.values('coin_symbol').annotate(
            watchers_count=Count('user')
        ).order_by('-watchers_count')

class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='crypto_posts')
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='posts/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_posts', blank=True)
    coin_symbol = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.title}"

    def total_likes(self):
        return self.likes.count()

class Investment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='investments')
    coin_symbol = models.CharField(max_length=10)
    amount = models.DecimalField(max_digits=20, decimal_places=8)
    price_at_purchase = models.DecimalField(max_digits=20, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'coin_symbol']

    def __str__(self):
        return f"{self.user.username} - {self.coin_symbol} - {self.amount}"
