from persiantools.jdatetime import JalaliDateTime
from rest_framework import serializers
from site_settings.models import SiteSettings


class SiteSettingsSerializer(serializers.ModelSerializer):

    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    class Meta:
        model = SiteSettings
        fields = ['title', 'url', 'gmail', 'phone', 'logo', 'about', 'description', 'contact', 'address', 'manager', 'is_active', 'created_at', 'updated_at']

    def get_created_at(self, obj):
        if not obj.created_at:
            return None
        jdt = JalaliDateTime.to_jalali(obj.created_at)
        return jdt.strftime("%Y/%m/%d %H:%M:%S")

    def get_updated_at(self, obj):
        if not obj.updated_at:
            return None
        jdt = JalaliDateTime.to_jalali(obj.updated_at)
        return jdt.strftime("%Y/%m/%d %H:%M:%S")
