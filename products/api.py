from rest_framework import generics
from .serializers import (ProductListSerializer, ProductDetailSerializer,
                          BrandListSerializer, BrandDetailSerializer)
from .models import Product, Brand
from .pagination import BrandPagination
from django_filters import rest_framework
from rest_framework import filters


class ProductListAPI(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    filter_backends = [rest_framework.DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['flag', 'brand']
    search_fields = ['name', 'sku', 'subtitle', 'description']


class ProductDetailAPI(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer


class BrandListAPI(generics.ListAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandListSerializer
    pagination_class = BrandPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class BrandDetailAPI(generics.RetrieveAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandDetailSerializer
