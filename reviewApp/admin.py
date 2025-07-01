from django.contrib import admin
from .models import User, MovieReview
from .models import BlockedIP #for IP Blocking model

admin.site.register(User)
admin.site.register(MovieReview)

 
#register the BlockedIP model
admin.site.register(BlockedIP)