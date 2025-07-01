from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import FitnessEntry, User
from datetime import timedelta, date
from django.core.mail import send_mail
from django.conf import settings


@receiver(post_save, sender=FitnessEntry)
def update_streak(sender, instance, created, **kwargs):
    if not created:
        return

    user = instance.user
    today = date.today()

    # Get all dates the user worked out
    entries = FitnessEntry.objects.filter(user=user).values_list('date', flat=True).distinct()
    dates = sorted(entries, reverse=True)

    # Calculate streak
    streak = 0
    for i, entry_date in enumerate(dates):
        expected_date = today - timedelta(days=i)
        if entry_date == expected_date:
            streak += 1
        else:
            break

    user.streak_count = streak
    user.save()

@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        subject = 'Welcome to Fitness Tracker!'
        message = f'Hi {instance.username},\n\nThanks for registering with Fitness Tracker. Get ready to track your activities and stay fit!'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [instance.email]

        send_mail(subject, message, from_email, recipient_list, fail_silently=False)