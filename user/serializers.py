from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import Serializer

from user.validators import phone_validator, english_validator, persian_validator

User = get_user_model()


class UserLoginSerializer(Serializer):
    phone = serializers.CharField(validators=[phone_validator], max_length=12, min_length=12)
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


class RegisterSerializer(Serializer):
    phone = serializers.CharField(validators=[phone_validator], max_length=12, min_length=12)
    username = serializers.CharField(validators=[english_validator, ])
    first_name = serializers.CharField(validators=[persian_validator, ])
    last_name = serializers.CharField(validators=[persian_validator, ])
    email = serializers.EmailField(required=False)
    password = serializers.CharField()
    confirm_password = serializers.CharField()

    def validate_phone(self, data):
        if data:
            user = User.objects.filter(phone=data)
            if user.exists():
                raise serializers.ValidationError(_('Phone number already in use'))
        return data

    def validate_username(self, data):
        if data:
            user = User.objects.filter(username=data)
            if user.exists():
                raise serializers.ValidationError(_('Username already in use'))
        return data

    def validate(self, data):

        password = data.get('password')
        confirm_password = data.get('confirm_password')

        if password != confirm_password:
            raise ValidationError(_("Your passwords didn't match."))

        return data
