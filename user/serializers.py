from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.serializers import Serializer

User = get_user_model()

PHONE_REGEX = RegexValidator(
    regex=r"^989\d{2}\s*?\d{3}\s*?\d{4}$", message=_("Invalid phone number."),
)


class UserLoginSerializer(Serializer):
    phone = serializers.CharField(validators=[PHONE_REGEX], max_length=12, min_length=12)
    password = serializers.CharField()

    def validate(self, data):
        phone = data.get('phone')
        password = data.get('password')

        try:
            user = User.objects.get(phone=phone)
        except User.DoesNotExist:
            raise serializers.ValidationError(_('Phone number not found'))

        if not check_password(password, user.password):
            raise serializers.ValidationError(_('Password or Phone number incorrect'))

        return data
