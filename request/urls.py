from django.urls import path

from request import views

urlpatterns = [
    path('consulting/', views.UserRequestConsultingAPIView.as_view(), name='user-request-consulting'),
    path('spraying/', views.UserRequestSprayingAPIView.as_view(), name='user-request-spraying'),
    path('', views.UserRequestPanelAPIView.as_view(), name='user-request-panel'),
]
