from django.contrib.auth import get_user_model
from rest_framework import permissions
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
    http_method_names = ['get', 'put', 'patch', 'delete']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAdminPanelPermission(), ]
        elif self.action in ['destroy', 'update', 'partial_update']:
            return [IsSuperAdminPanelPermission(), ]
        return super().get_permissions()
