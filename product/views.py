from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.db.models.aggregates import Count
from rest_framework import permissions, status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response

from admin_panel.models import AdminPanel
from product.models import Product
from product.serializers import ProductAllFieldSerializer, ProductShowSerializer


class ProductListCreateView(ListCreateAPIView):
    def get_serializer_class(self):
        if self.request.user.is_authenticated:
            is_admin = self.request.user.is_superuser or self.request.user.is_staff or self.request.user.is_admin
        else:
            is_admin = False
        if is_admin:
            return ProductAllFieldSerializer
        else:
            return ProductShowSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny(), ]
        else:
            return [permissions.IsAuthenticated(), permissions.IsAdminUser()]

    def get_queryset(self):
        q = Product.objects.all().prefetch_related('tags')
        params = self.request.GET
        search = params.get('search')
        tags = params.getlist('tags')
        try:
            if search:
                search_vector = SearchVector('title', weight='A') + SearchVector('tags', weight='B') + SearchVector(
                    'description', weight='C')
                search_query = SearchQuery(search)
                q = (
                    q.annotate(rank=SearchRank(search_vector, search_query))
                    .filter(rank__gte=0.1)
                    .order_by("-rank")
                )
            if tags:
                q = q.filter(tags__name__in=tags).distinct()
            return q
        except Exception as e:
            return Product.objects.none()


class ProductDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all().prefetch_related('tags')
    lookup_url_kwarg = 'slug'
    lookup_field = 'slug'

    def get_serializer_class(self):
        if self.request.user.is_authenticated:
            is_admin = self.request.user.is_superuser or self.request.user.is_staff or self.request.user.is_admin
        else:
            is_admin = False
        if is_admin:
            return ProductAllFieldSerializer
        else:
            return ProductShowSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny(), ]
        else:
            return [permissions.IsAuthenticated(), permissions.IsAdminUser()]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        tags = instance.tags.all()
        same_products = (
            Product.objects.filter(tags__in=tags).annotate(same_tags=Count('tags'))
            .exclude(id=instance.id)
            .distinct().order_by('-same_tags', '-created_at')[:5]
        )

        same_products_data = ProductShowSerializer(same_products, many=True, context={"request": request}).data

        data = {
            "product": self.get_serializer(instance).data,
            "same_products": same_products_data
        }

        return Response(data, status=status.HTTP_200_OK)
