from rest_framework import serializers
from user.validators import phone_validator
from request.models import Request


class UserRequestConsultingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = ['phone', 'message']


    def validate_phone(self, value):
        phone_validator(value)
        return value