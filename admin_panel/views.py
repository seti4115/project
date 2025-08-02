from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from admin_panel.serializers import AllSerializer, UserDetailSerializer
from .permissions import ISAdminPanelPermission

User = get_user_model()


class AdminPanelAPIView(APIView):
    permission_classes = [ISAdminPanelPermission]

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
    serializer_class = UserDetailSerializer
    http_method_names = ['get', 'put', 'delete']

