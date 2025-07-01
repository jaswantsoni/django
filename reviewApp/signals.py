#signals notes
# sender-modal
# receiver-handles the signal
# .signal()
# add in apps.py add reviewApp.signals()

#from django.dispatch import Signal


from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import MovieReview

@receiver(post_save, sender=MovieReview)
def review_posted(sender, instance, created, **kwargs):
    if created:
        print(f"##################### New review posted: {instance.movie_title} by {instance.author.username}")
