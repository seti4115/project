from django.contrib.auth import get_user_model
from rest_framework import serializers

from request.serializers import ViewRequestConsultingSerializer, ViewSprayingRequestSerializer
from user.serializers import UserDetailSerializer

User = get_user_model()



class UserEditSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ['phone', 'username', 'email', 'first_name', 'last_name', 'is_active', 'is_admin']


class AllSerializer(serializers.Serializer):
    users =                         UserDetailSerializer(many=True)
    consulting_requests = ViewRequestConsultingSerializer(many=True)
    spraying_requests = ViewSprayingRequestSerializer(many=True)
