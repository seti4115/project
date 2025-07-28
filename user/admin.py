from django.contrib import admin

from .models import User


# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser']
    list_editable = ['is_active', 'is_staff', 'is_superuser']
    ordering = ['-id', 'is_active']

