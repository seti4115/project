from rest_framework import serializers

from request.models import Request


class UserRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = ['phone', 'message']