from django.urls import path, include
from rest_framework.routers import SimpleRouter

from admin_panel import views

router = SimpleRouter()
router.register(r'users', views.UserListAdminPanel, basename='user-list')
urlpatterns = [
    path('', views.AdminPanelAPIView.as_view(), name='admin-panel'),
    path('', include(router.urls)),
]
