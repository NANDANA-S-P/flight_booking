from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser

class CustomUserAdmin(UserAdmin):
     list_display = (
        'username', 'email', 'first_name', 'last_name', 'is_staff',
        'is_verified'
        )
    

admin.site.register(CustomUser, CustomUserAdmin)