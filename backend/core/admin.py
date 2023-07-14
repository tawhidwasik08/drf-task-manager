from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'role', 'email')