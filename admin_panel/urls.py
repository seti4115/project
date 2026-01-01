from django.urls import path, include
from rest_framework.routers import SimpleRouter

from admin_panel import views


urlpatterns = [
    path('', views.AdminPanelAPIView.as_view(), name='admin-panel'),
    path('consulting/', views.ConsultingListAdminPanelView.as_view(), name='consulting-list-create'),
    path('spraying/', views.SprayingListAdminPanelView.as_view(), name='spraying-list-create'),
    path('consulting/<int:pk>/', views.RetrieveUpdateDestroyConsultingAdminPanel.as_view(), name='consulting-detail-update-destroy'),
    path('spraying/<int:pk>/', views.RetrieveUpdateDestroySprayingAdminPanel.as_view(), name='spraying-detail-update-destroy'),
    path('users/', views.UserListAdminPanel.as_view(), name='user-list-create' ),
    path('users/<pk>/', views.UserDetailUpdateDestroyAdminPanel.as_view(), name='user-detail' ),
    path('isadmin/', views.IsAdminPanel.as_view(), name='is_admin'),
]
