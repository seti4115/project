from django.contrib.auth import get_user_model
from rest_framework import permissions, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from admin_panel.serializers import AllSerializer, UserDetailSerializer, UserEditSerializer
from .permissions import IsAdminPanelPermission, IsSuperAdminPanelPermission

User = get_user_model()


class AdminPanelAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsAdminPanelPermission]

    def get(self, request, *args, **kwargs):
        users = User.objects.all()
        serializer = AllSerializer(
            {
                'users': UserDetailSerializer(users, many=True).data,
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
