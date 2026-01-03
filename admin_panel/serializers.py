from django.contrib.auth import get_user_model
from persiantools.jdatetime import JalaliDateTime
from rest_framework import serializers

from request.serializers import ViewRequestConsultingSerializer, ViewSprayingRequestSerializer
from user.serializers import UserDetailSerializer
from user.validators import english_validator

User = get_user_model()


class UserEditSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(read_only=True)
    date_joined = serializers.SerializerMethodField(source="get_date_joined", read_only=True)
    new_password = serializers.CharField(allow_blank=True, write_only=True, allow_null=True, required=False,
                                         label="پسورد جدید", validators=[english_validator])
    old_password = serializers.CharField(allow_blank=True, write_only=True, allow_null=True, required=False,
                                         label="تکرار پسورد جدید", validators=[english_validator])

    class Meta:
        model = User
        fields = ['id', 'phone', 'username', 'email', 'first_name', 'last_name', 'is_active', 'is_admin', 'date_joined',
                  'new_password', 'old_password']
        read_only_fields = ['id']

    def validate(self, attrs):
        new_password = attrs.get('new_password')
        old_password = attrs.get('old_password')
        if new_password:
            if new_password == old_password:
                if len(new_password) >= 6:
                    user = User.objects.get(username=attrs['username'])
                    user.set_password(new_password)
                    user.save()
            else:
                raise serializers.ValidationError("لطفا پسورد معتبر وارد کنید.")
        return attrs

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
