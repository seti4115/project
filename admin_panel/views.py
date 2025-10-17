from django.contrib.auth import get_user_model
from rest_framework import permissions, filters, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from admin_panel.serializers import AllSerializer, UserDetailSerializer, UserEditSerializer
from request.models import ConsultingRequest, SprayingRequest
from request.serializers import ViewRequestConsultingSerializer, ViewSprayingRequestSerializer
from .models import AdminPanel
from .permissions import IsAdminPanelPermission, IsSuperAdminPanelPermission

User = get_user_model()


class AdminPanelAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsAdminPanelPermission]

    def get(self, request, *args, **kwargs):
        print(request.GET)
        users = User.objects.all()
        consulting_requests = ConsultingRequest.objects.all().order_by("-created_at")
        spraying_requests = SprayingRequest.objects.all().order_by("-created_at")
        serializer = AllSerializer(
            {
                "users": UserDetailSerializer(users, many=True).data,
                "consulting_requests": ViewRequestConsultingSerializer(consulting_requests, many=True).data,
                "spraying_requests": ViewSprayingRequestSerializer(spraying_requests, many=True).data,
            }
        )
        return Response(serializer.data)


class UserListAdminPanel(ModelViewSet):
    model = User
    queryset = User.objects.all()
    serializer_class = UserEditSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['username', 'phone', 'id', 'email', 'last_name']
    ordering_fields = ['phone', 'last_name', 'date_joined', 'last_login']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAdminPanelPermission(), ]
        elif self.action in ['destroy', 'update', 'partial_update']:
            return [IsSuperAdminPanelPermission(), ]
        return super().get_permissions()


class IsAdminPanel(APIView):
    def get(self, request, *args, **kwargs):
        user = request.user
        admin = AdminPanel.objects.filter(user=user).exists()
        return Response({'admin': admin}, status=status.HTTP_200_OK)
