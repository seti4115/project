from django.contrib import admin, messages

from admin_panel.models import AdminPanel
from .models import User


class AdminPanelInline(admin.StackedInline):
    model = AdminPanel
    can_delete = False
    extra = 0
    max_num = 1


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser']
    list_editable = ['is_active', 'is_staff', 'is_superuser']
    ordering = ['-id', 'is_active']
    inlines = [AdminPanelInline]
    #
    # def save_model(self, request, obj, form, change):
    #
    #     if obj.is_admin and not hasattr(obj, 'adminpanel'):
    #         AdminPanel.objects.create(user=obj)
    #
    #     if not obj.is_admin and hasattr(obj, 'adminpanel'):
    #         AdminPanel.objects.get(user=obj).delete()
    #
    #     return super(UserAdmin, self).save_model(request, obj, form, change)