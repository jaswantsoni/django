#custom decorator to make sure only verifiried user post review here
from django.contrib.auth.decorators import user_passes_test

def is_verified(user):
    return user.is_authenticated and user.is_verified

verified_required = user_passes_test(is_verified, login_url='/not-verified/')
