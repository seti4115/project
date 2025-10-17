from rest_framework import serializers

from user.serializers import UserDetailSerializer
from request.models import ConsultingRequest, SprayingRequest
from user.validators import phone_validator, persian_validator


class UserRequestConsultingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsultingRequest
        fields = ['first_name', 'last_name', 'phone', 'province', 'city', 'land_product', 'message']

    def validate_phone(self, value):
        phone_validator(value)
        return value

    def validate(self, data):
        first_name = data['first_name']
        last_name = data['last_name']
        persian_validator(first_name)
        persian_validator(last_name)
        return data


class ViewRequestConsultingSerializer(serializers.ModelSerializer):
    status = serializers.CharField(source='get_status_display', read_only=True)
    user = UserDetailSerializer(read_only=True)

    class Meta:
        model = ConsultingRequest
        fields = ["type", "first_name", "last_name", "phone", "province", "city", "land_product", "created_at", "status", "message", "user"]

    def get_status_display(self, obj):
        return obj.get_status_display()


class SprayingRequestSerializer(serializers.ModelSerializer):
    message = serializers.CharField(required=False, allow_blank=True, default="")

    class Meta:
        model = SprayingRequest
        fields = ['first_name', 'last_name', 'phone', 'province', 'city', 'land_product', 'land_area', 'address', 'message']


class ViewSprayingRequestSerializer(serializers.ModelSerializer):
    status = serializers.CharField(source='get_status_display', read_only=True)
    user = UserDetailSerializer(read_only=True)

    class Meta:
        model = SprayingRequest
        fields = ["type", "first_name", "last_name", "phone", "province", "city", "land_product", "created_at", "status", "land_area", "address", "message", "user"]

    def get_status_display(self, obj):
        return obj.get_status_display()
