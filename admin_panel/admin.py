from django.contrib import admin
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from admin_panel.models import AdminPanel, Access


@admin.register(AdminPanel)
class AdminPanelAdmin(admin.ModelAdmin):
    pass