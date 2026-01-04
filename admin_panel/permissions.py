from rest_framework.permissions import BasePermission

from admin_panel.models import Access, AdminPanel


class IsAdminPanelPermission(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        try:
            print(request.user.adminpanel.access in [Access.admin])
            return request.user.adminpanel.access in [Access.admin]
        except AdminPanel.DoesNotExist:
            return False


class IsSuperAdminPanelPermission(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        try:
            print(request.user.adminpanel.access in [Access.superuser])
            return request.user.adminpanel.access in [Access.superuser]
        except AdminPanel.DoesNotExist:
            return False

class IsFrontAdminPanelPermission(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        try:
            return request.user.adminpanel.access in [Access.admin, Access.superuser]
        except AdminPanel.DoesNotExist:
            return False
