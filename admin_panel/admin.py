from django.contrib import admin
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from admin_panel.models import AdminPanel, Access


@admin.register(AdminPanel)
class AdminPanelAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if obj.access == Access.superuser.value:
            obj.is_superuser = True
        if obj.access == Access.admin.value:
            obj.is_staff = True
        return super().save_model(request, obj, form, change)