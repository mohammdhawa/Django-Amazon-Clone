from rest_framework import generics
from .serializers import (ProductListSerializer, ProductDetailSerializer,
                          BrandListSerializer, BrandDetailSerializer)
from .models import Product, Brand
from .pagination import BrandPagination
from django_filters import rest_framework


class ProductListAPI(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    filter_backends = [rest_framework.DjangoFilterBackend]
    filterset_fields = ['flag', 'brand']


class ProductDetailAPI(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer


class BrandListAPI(generics.ListAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandListSerializer
    pagination_class = BrandPagination


class BrandDetailAPI(generics.RetrieveAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandDetailSerializer
