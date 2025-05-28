from django.contrib import admin
from .models import User, Post, Comments

admin.site.register(User)
admin.site.register(Post)
admin.site.register(Comments)

# Register your models here.
