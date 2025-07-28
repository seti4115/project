from django.urls import path

from user import views

urlpatterns = [
    path('login/', views.LoginAPIView.as_view(), name='login'),
]