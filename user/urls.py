from django.urls import path

from user import views

urlpatterns = [
    path('profile/', views.UserProfileAPIView.as_view(), name='profile'),
    path('login/', views.LoginAPIView.as_view(), name='login'),
    path('auth/', views.AuthStatusAPIView.as_view(), name='auth-status'),
    path('register/', views.RegisterAPIView.as_view(), name='register'),
]
