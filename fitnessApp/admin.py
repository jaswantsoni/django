from django.contrib import admin
from .models import User, FitnessEntry
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        (None, {'fields': ('phone_number', 'age')}),
    )

admin.site.register(User, UserAdmin)
admin.site.register(FitnessEntry)