from django.contrib import admin

from .models import ConsultingRequest, SprayingRequest


@admin.register(ConsultingRequest)
class ConsultingRequestAdmin(admin.ModelAdmin):
    list_display = ['phone', 'type', 'status', 'created_at']

@admin.register(SprayingRequest)
class SprayingRequestAdmin(admin.ModelAdmin):
    list_display = ['phone', 'type', 'status', 'created_at']