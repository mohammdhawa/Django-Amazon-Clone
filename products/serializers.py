from rest_framework import serializers
from .models import Product, Brand, Review, ProductImages


class ProductImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImages
        fields = ("image",)


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Review
        fields = ("user", "review", "rate", "created_at")


class ProductListSerializer(serializers.ModelSerializer):
    brand = serializers.StringRelatedField()

    class Meta:
        model = Product
        fields = ('name', 'flag', 'price', 'image', 'sku', 'subtitle', 'description',
                  'brand', 'reviews_count', 'avg_rate')


class ProductDetailSerializer(serializers.ModelSerializer):
    brand = serializers.StringRelatedField()
    images = ProductImagesSerializer(source='product_images', many=True)
    reviews = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('name', 'flag', 'price', 'image', 'sku', 'subtitle', 'description',
                  'brand', 'reviews_count', 'avg_rate', 'images', 'reviews')

    def get_reviews(self, obj):
        reviews = obj.product_review.all()
        return ReviewSerializer(reviews, many=True).data


class BrandListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'


class BrandDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'
