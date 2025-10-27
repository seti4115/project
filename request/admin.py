from django.contrib import admin
from persiantools.jdatetime import JalaliDateTime

from .models import ConsultingRequest, SprayingRequest


@admin.register(ConsultingRequest)
class ConsultingRequestAdmin(admin.ModelAdmin):
    list_display = ['phone', 'status', 'created_at_to_jalali']
    list_filter = ['status', 'created_at']
    list_editable = ['status']

    def created_at_to_jalali(self, obj):
        jdt = JalaliDateTime.to_jalali(obj.created_at)
        return jdt.strftime("%H:%M  %Y/%m/%d")

    created_at_to_jalali.short_description = "ایجاد شده در"


@admin.register(SprayingRequest)
class SprayingRequestAdmin(admin.ModelAdmin):
    list_display = ['phone', 'type', 'status', 'created_at_to_jalali']
    list_filter = ['status', 'created_at']
    list_editable = ['status']

    def created_at_to_jalali(self, obj):
        jdt = JalaliDateTime.to_jalali(obj.created_at)
        return jdt.strftime("%H:%M  %Y/%m/%d")

    created_at_to_jalali.short_description = "ایجاد شده در"
