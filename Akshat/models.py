from django.db import models
from django.contrib.auth.models import AbstractUser



class User(AbstractUser):
    joined_ad = models.DateTimeField(auto_now_add=True)
    phone = models.CharField(max_length=15)
    dp = models.FileField(upload_to='uploads/')
    def __str__(self):
        return self.username


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    content = models.TextField()
    tags = models.CharField(max_length=30)
    created_at  = models.DateTimeField(auto_now_add=True)
    image = models.FileField(upload_to='uploads/')

    def __str__(self):
        return  self.post


class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment





