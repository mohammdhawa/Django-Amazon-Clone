from rest_framework import generics
from .serializers import (ProductListSerializer, ProductDetailSerializer,
                          BrandListSerializer, BrandDetailSerializer)
from .models import Product, Brand
from .pagination import BrandPagination


class ProductListAPI(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer


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
