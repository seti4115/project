from django.urls import path

from user import views

urlpatterns = [
    path('reset-password/', views.ForgotPasswordAPIView.as_view(), name='forgot_password'),
    path('reset-password/<uidb64>/<token>/', views.ResetPasswordAPIView.as_view(), name='reset_password'),
    path('profile/', views.UserProfileAPIView.as_view(), name='profile'),
    path('login/', views.LoginAPIView.as_view(), name='login'),
    path('register/', views.RegisterAPIView.as_view(), name='register'),
]
