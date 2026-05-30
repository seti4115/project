from django.urls import path, include
from rest_framework.routers import SimpleRouter

from admin_panel import views


urlpatterns = [
    path('', views.AdminPanelAPIView.as_view(), name='home-adminpanel'),
    path('admins/', views.ListCreateAdminPanelAPIView.as_view(), name='admin-panel-create-list-adminpanel'),
    path('site/', views.SiteSettingsAdminPanelView.as_view(), name='site-settings-create-list-adminpanel'),
    path('consulting/', views.ConsultingListAdminPanelView.as_view(), name='consulting-list-create-adminpanel'),
    path('spraying/', views.SprayingListAdminPanelView.as_view(), name='spraying-list-create-adminpanel'),
    path('users/', views.UserListAdminPanel.as_view(), name='user-list-create-adminpanel' ),
    path('products/', views.ListCreateProductAdminPanelAPIView.as_view(), name='product-list-create-adminpanel' ),
    path('isadmin/', views.IsAdminPanel.as_view(), name='is_admin'),
    path('admins/<pk>/', views.RetrieveUpdateDestroyAdminPanelAPIView.as_view(), name='admin-panel-detail-adminpanel'),
    path('site/<pk>/', views.RetrieveUpdateDestroySiteSettingsAdminPanelAPIView.as_view(), name='site-settings-detail-adminpanel'),
    path('consulting/<int:pk>/', views.RetrieveUpdateDestroyConsultingAdminPanel.as_view(), name='consulting-detail-update-destroy-adminpanel'),
    path('spraying/<int:pk>/', views.RetrieveUpdateDestroySprayingAdminPanel.as_view(), name='spraying-detail-update-destroy-adminpanel'),
    path('users/<pk>/', views.UserDetailUpdateDestroyAdminPanel.as_view(), name='user-detail-adminpanel' ),
    path('users/<pk>/changepassword/', views.ChangePassUserAdminPanelView.as_view(), name='user-detail-adminpanel' ),
    path('products/<slug:slug>/', views.RetrieveUpdateDestroyProductAdminPanelAPIView.as_view(), name='product-detail-adminpanel' ),
]
