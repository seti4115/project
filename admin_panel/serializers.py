from django.contrib.auth import get_user_model
from persiantools.jdatetime import JalaliDateTime
from rest_framework import serializers

from admin_panel.models import AdminPanel
from request.serializers import ViewRequestConsultingSerializer, ViewSprayingRequestSerializer
from user.serializers import UserDetailSerializer
from user.validators import english_validator

User = get_user_model()


class UserEditSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(read_only=True)
    profile_link = serializers.SerializerMethodField(read_only=True)
    date_joined = serializers.SerializerMethodField(source="get_date_joined",read_only=True)

    class Meta:
        model = User
        fields = ['id', 'phone', 'username', 'email', 'first_name', 'last_name', 'is_active', 'is_admin', 'date_joined',
                  'profile_link']
        read_only_fields = ['id']

    def get_date_joined(self, obj):
        if not obj.date_joined:
            return None
        jdt = JalaliDateTime.to_jalali(obj.date_joined)
        return jdt.strftime("%Y/%m/%d %H:%M:%S")

    def get_profile_link(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.get_absolute_url())


class AllSerializer(serializers.Serializer):
    users = UserDetailSerializer(many=True)
    consulting_requests = ViewRequestConsultingSerializer(many=True)
    spraying_requests = ViewSprayingRequestSerializer(many=True)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'phone', 'first_name', 'last_name', 'is_active', 'is_admin',]


class AdminPanelSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='user',
        write_only=True
    )

    class Meta:
        model = AdminPanel
        fields = ['user', 'user_id','id' ,'access']


class ChangePassUserAdminPanelSerializer(serializers.Serializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def validate(self, attrs):
        if attrs.get('password1') != attrs.get('password2'):
            raise serializers.ValidationError("Passwords must match")
        return attrs