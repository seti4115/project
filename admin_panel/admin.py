from django.contrib import admin, messages
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from admin_panel.models import AdminPanel, Access


@admin.register(AdminPanel)
class AdminPanelAdmin(admin.ModelAdmin):
    list_display = ('user', 'access')
    list_editable = ('access',)

        
