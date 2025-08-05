from django.contrib import admin

from .models import ConsultingRequest


@admin.register(ConsultingRequest)
class RequestAdmin(admin.ModelAdmin):
    list_display = ['phone', 'type', 'status', 'created_at']
