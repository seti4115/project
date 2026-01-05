from django.contrib import admin

from log.models import Log


# Register your models here.
@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ["id", "level", "views", "status_code", "action", "from_user", "created_at"]