from rest_framework import serializers

from request.models import ConsultingRequest
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
    class Meta:
        model = ConsultingRequest
        fields = ['id', 'land_product', 'message', 'status', 'created_at']
