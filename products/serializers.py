from rest_framework import serializers
from .models import Product, Brand, Review, ProductImages
from taggit.serializers import (TagListSerializerField,
                                TaggitSerializer)


class ProductImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImages
        fields = ("image",)


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Review
        fields = ("user", "review", "rate", "created_at")


class ProductListSerializer(TaggitSerializer, serializers.ModelSerializer):
    brand = serializers.StringRelatedField()
    tags = TagListSerializerField()

    class Meta:
        model = Product
        fields = ('id', 'name', 'flag', 'price', 'image', 'sku', 'subtitle', 'description',
                  'brand', 'reviews_count', 'avg_rate', 'tags')


class ProductDetailSerializer(TaggitSerializer, serializers.ModelSerializer):
    brand = serializers.StringRelatedField()
    images = ProductImagesSerializer(source='product_images', many=True)
    reviews = ReviewSerializer(source='product_review', many=True)
    tags = TagListSerializerField()

    class Meta:
        model = Product
        fields = ('id', 'name', 'flag', 'price', 'image', 'sku', 'subtitle', 'description',
                  'brand', 'reviews_count', 'avg_rate', 'images', 'reviews', 'tags')


class BrandListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'


class BrandDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'
