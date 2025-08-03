from django.urls import path

from request import views

urlpatterns = [
    path('consulting/', views.UserRequestConsultingAPIView.as_view(), name='user-request-consulting'),
]