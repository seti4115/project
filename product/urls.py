from django.urls import path

from product.views import ProductDetailAPIView, ProductListCreateView

urlpatterns = [
    path('products/<slug:slug>/', ProductDetailAPIView.as_view(), name='product-detail'),
    path('products/', ProductListCreateView.as_view(), name='product-list'),
]