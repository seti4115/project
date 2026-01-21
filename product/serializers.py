from persiantools.jdatetime import JalaliDateTime
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from taggit.serializers import TaggitSerializer, TagListSerializerField, TagList

from product.models import Product


class ProductAllFieldSerializer(TaggitSerializer, ModelSerializer):
    link = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    def get_updated_at(self, obj):
        if not obj.updated_at:
            return None
        jdt = JalaliDateTime.to_jalali(obj.updated_at)
        return jdt.strftime("%Y/%m/%d %H:%M:%S")

    def get_link(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.get_absolute_url())

    def get_created_at(self, obj):
        if not obj.created_at:
            return None
        jdt = JalaliDateTime.to_jalali(obj.created_at)
        return jdt.strftime("%Y/%m/%d %H:%M:%S")

    class Meta:
        model = Product
        fields = [
            'title',
            'title_en',
            'slug',
            'weight',
            'type',
            'brand',
            'description',
            'price',
            'production_date',
            'expiration_date',
            'is_active',
            'created_at',
            'updated_at',
            'link',
        ]


class ProductShowSerializer(TaggitSerializer, ModelSerializer):
    link = serializers.SerializerMethodField()
    tags = TagListSerializerField()
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    def get_updated_at(self, obj):
        if not obj.updated_at:
            return None
        jdt = JalaliDateTime.to_jalali(obj.updated_at)
        return jdt.strftime("%Y/%m/%d %H:%M:%S")

    def get_created_at(self, obj):
        if not obj.created_at:
            return None
        jdt = JalaliDateTime.to_jalali(obj.created_at)
        return jdt.strftime("%Y/%m/%d %H:%M:%S")

    def get_link(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.get_absolute_url())

    class Meta:
        model = Product
        fields = ['title', 'link', 'weight', 'type', 'brand', 'description', 'price', 'production_date',
                  'expiration_date','created_at', 'updated_at', 'is_active']

