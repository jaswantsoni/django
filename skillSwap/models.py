from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    is_verified = models.BooleanField(default=False)
    bio = models.TextField(blank=True, null=True)
    skills_can_teach = models.ManyToManyField("Skill", related_name="teachers")
    skills_want_to_learn = models.ManyToManyField("Skill", related_name="learners")

class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)

class SkillSession(models.Model):
    teacher = models.ForeignKey(User, related_name='sessions_taught', on_delete=models.CASCADE)
    learner = models.ForeignKey(User, related_name='sessions_attended', on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    summary_file = models.FileField(upload_to='session_summaries/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.learner.username} ↔ {self.teacher.username} - {self.skill.name}"

class Rating(models.Model):
    session = models.OneToOneField(SkillSession, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()  # 1–5
    feedback = models.TextField(blank=True, null=True)
