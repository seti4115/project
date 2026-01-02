from django.contrib import admin, messages
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from admin_panel.models import AdminPanel, Access


@admin.register(AdminPanel)
class AdminPanelAdmin(admin.ModelAdmin):
    list_display = ('user', 'access')
    list_editable = ('access',)

    def delete_model(self, request, obj):
        obj.user.is_admin = False
        obj.user.save()
        obj.delete()
        return super().delete_model(request, obj)

    def save_model(self, request, obj, form, change):
        obj.user.is_admin = True
        obj.user.save()
        return super().save_model(request, obj, form, change)
    
    def delete_queryset(self, request, queryset):
        for q in queryset:
            q.user.is_admin = False
            q.user.save()
        return super().delete_queryset(request, queryset)
        
