from django.contrib import admin

from site_settings.models import SiteSettings


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ['pk', 'title', 'is_active']
    list_editable = ('is_active',)