from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    is_recruiter = models.BooleanField(default=False)
    email = models.EmailField(unique=True)
    REQUIRED_FIELDS = ["email"]


class JobPost(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    posted_by = models.ForeignKey(
        User, on_delete=models.CASCADE, limit_choices_to={"is_recruiter": True}
    )
    created_at = models.DateTimeField(auto_now_add=True)


class Application(models.Model):
    candidate = models.ForeignKey(
        User, on_delete=models.CASCADE, limit_choices_to={"is_recruiter": False}
    )
    cover_letter = models.TextField(blank=True, null=True)
    job_post = models.ForeignKey(JobPost, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def candidate_email(self):
        return self.candidate.email
