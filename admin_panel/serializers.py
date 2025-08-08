from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'phone']


class UserEditSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ['phone', 'username', 'email', 'first_name', 'last_name', 'is_active', 'is_admin']


class AllSerializer(serializers.Serializer):
    users = UserDetailSerializer(many=True)
