from rest_framework.permissions import BasePermission

from admin_panel.models import Access, AdminPanel


class IsAdminPanelPermission(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        try:
            return request.user.adminpanel.access in [Access.admin, Access.superuser]
        except AdminPanel.DoesNotExist:
            return False


class IsSuperAdminPanelPermission(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        try:
            return request.user.adminpanel.access == Access.superuser
        except AdminPanel.DoesNotExist:
            return False

class EditPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            if request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
                return True
            return False
        return False