#19th and 20th June 2025 by nisha

from django.dispatch import Signal, receiver
from django.db.models.signals import pre_save, post_save
from .models import Post, User, Comment

def mail(message):
    print(f"sending the mail with: {message}")

@receiver(post_save, sender=Post)
def send_mail(sender, instance, created, title):
    if created:
        mail("Thanks for creating a new post with us")

#custom signal
update=Signal(sender=Post, args1=['title'])
@receiver(update)
def update_handler(sender, **kwargs):
    title=kwargs.get('title')
    print(f"post table updated with title: {title}")
    mail(f"post table updated with title: {title}")

# can use it with review model where signal
# is generated while posting a review 



##########################3
# decoratore

def only_gmail(gmail_test):
    def wrapper(func):
        def inner(*args, **kwargs):
            if gmail_test.endswith('@gmail.com'):
                return func(*args, **kwargs)
            else:
                print("done")
                return None
        return inner
#using decorator
#@only_gmail(gmail_test)