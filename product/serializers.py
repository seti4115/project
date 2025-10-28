from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from taggit.serializers import TaggitSerializer, TagListSerializerField

from product.models import Product


class ProductAllFieldSerializer(TaggitSerializer, ModelSerializer):
    link = serializers.SerializerMethodField()
    tags = TagListSerializerField()

    def get_link(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.get_absolute_url())

    class Meta:
        model = Product
        fields = '__all__'


class ProductShowSerializer(TaggitSerializer, ModelSerializer):
    link = serializers.SerializerMethodField()
    tags = TagListSerializerField()

    class Meta:
        model = Product
        fields = ['title', 'link', 'weight', 'type', 'brand', 'description', 'price', 'production_date',
                  'expiration_date', 'tags']

    def get_link(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.get_absolute_url())
