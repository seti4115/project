from persiantools.jdatetime import JalaliDateTime
from rest_framework import serializers

from request.models import ConsultingRequest, SprayingRequest, Status
from user.serializers import UserDetailSerializer
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
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    user = UserDetailSerializer(read_only=True)

    class Meta:
        model = ConsultingRequest
        fields = ["id", "type", "first_name", "last_name", "phone", "province", "city", "land_product", "created_at",
                  "status", "message", "user", 'status_display']
        read_only_fields = ['id']

    def get_status_display(self, obj):
        return obj.get_status_display()


class RequestConsultingAdminPanelSerializer(serializers.ModelSerializer):
    status = serializers.ChoiceField(choices=Status.choices)
    created_at = serializers.SerializerMethodField()
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = ConsultingRequest
        fields = [
            "id", "type", "first_name", "last_name", "phone",
            "province", "city", "land_product", "created_at",
            "status", "status_display", "message", "user"
        ]
        read_only_fields = ["id", "status_display"]

    def get_status_display(self, obj):
        return obj.get_status_display()

    def get_created_at(self, obj):
        if not obj.created_at:
            return None
        jdt = JalaliDateTime.to_jalali(obj.created_at)
        return jdt.strftime("%Y/%m/%d %H:%M:%S")



class SprayingRequestSerializer(serializers.ModelSerializer):
    message = serializers.CharField(required=False, allow_blank=True, default="")
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = SprayingRequest
        fields = ['first_name', 'last_name', 'phone', 'province', 'city', 'land_product', 'land_area', 'address',
                  'message', 'status', 'status_display']

    def get_status_display(self, obj):
        return obj.get_status_display()


class ViewSprayingRequestSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    user = UserDetailSerializer(read_only=True)

    class Meta:
        model = SprayingRequest
        fields = ["id", "type", "first_name", "last_name", "phone", "province", "city", "land_product", "created_at",
                  "status", "land_area", "address", "message", "user", "status_display"]
        read_only_fields = ["id"]


    def get_status_display(self, obj):
        return obj.get_status_display()


class SprayingRequestAdminPanelSerializer(serializers.ModelSerializer):
    status = serializers.ChoiceField(choices=Status.choices)
    status_display = serializers.CharField(source='get_status_display')
    user = UserDetailSerializer(read_only=True)

    class Meta:
        model = SprayingRequest
        fields = ["id", "type", "first_name", "last_name", "phone", "province", "city", "land_product", "created_at",
                  "status", "status_display", "land_area", "address", "message", "user"]
        read_only_fields = ["id"]

    def get_status_display(self, obj):
        return obj.get_status_display()
