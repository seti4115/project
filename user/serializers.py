from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import Serializer

from user.validators import phone_validator, english_validator, persian_validator

User = get_user_model()


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'phone']


class UserLoginSerializer(Serializer):
    phone = serializers.CharField(validators=[phone_validator], max_length=12, min_length=12)
    password = serializers.CharField()

    def validate(self, data):
        phone = data.get('phone')
        password = data.get('password')

        try:
            user = User.objects.get(phone=phone)
        except User.DoesNotExist:
            raise serializers.ValidationError(_('کاربری با این شماره تلفن یافت نشد!'))

        if not check_password(password, user.password):
            raise serializers.ValidationError(_('شماره تلفن یا رمز عبور اشتباه می باشد!'))

        return data


class RegisterSerializer(Serializer):
    phone = serializers.CharField(validators=[phone_validator], max_length=12, min_length=12)
    username = serializers.CharField(validators=[english_validator, ], min_length=5, max_length=30)
    first_name = serializers.CharField(validators=[persian_validator, ])
    last_name = serializers.CharField(validators=[persian_validator, ])
    email = serializers.EmailField(required=False, allow_blank=True, default="")
    password = serializers.CharField(min_length=8, max_length=30, validators=[english_validator, ])
    confirm_password = serializers.CharField(validators=[english_validator, ], min_length=8, max_length=30)

    def validate_phone(self, data):
        if data:
            user = User.objects.filter(phone=data)
            if user.exists():
                raise serializers.ValidationError(_('این شماره تلفن قبلا ثبت شده است!'))
        return data

    def validate_username(self, data):
        if data:
            user = User.objects.filter(username=data)
            if user.exists():
                raise serializers.ValidationError(_('این نام کاربری قبلا ثبت شده است!'))
        return data

    def validate(self, data):

        password = data.get('password')
        confirm_password = data.get('confirm_password')

        if password != confirm_password:
            raise ValidationError(_("رمز عبور و تکرار رمز عبور مطابقت ندارد!"))

        return data


class ProfileSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(read_only=True)
    first_name = serializers.CharField(allow_blank=True)
    last_name = serializers.CharField(allow_blank=True)
    last_name = serializers.CharField(allow_blank=True)
    username = serializers.CharField(allow_blank=True)
    email = serializers.EmailField(allow_blank=True)
    date_joined = serializers.DateTimeField(read_only=True)

    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'username', 'phone', 'email', 'date_joined'
        ]


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField()
    confirm_password = serializers.CharField()

    def validate(self, data):
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        if password != confirm_password:
            raise ValidationError(_('رمز عبور و تکرار رمز عبور مطابقت ندارد!'))
        return data
