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
    reviews_count = serializers.SerializerMethodField()
    avg_rate = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'

    def get_reviews_count(self, obj):
        reviews = obj.reviews_count()
        return reviews

    def get_avg_rate(self, obj):
        avg = obj.avg_rate()
        return avg


class ProductDetailSerializer(serializers.ModelSerializer):
    brand = serializers.StringRelatedField()
    reviews_count = serializers.SerializerMethodField()
    avg_rate = serializers.SerializerMethodField()
    images = ProductImagesSerializer(source='product_images', many=True)
    reviews = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'

    def get_reviews_count(self, obj):
        reviews = obj.product_review.all().count()
        return reviews

    def get_avg_rate(self, obj):
        reviews = obj.product_review.all()
        if reviews:
            total_rates = sum(review.rate for review in reviews)
            average = total_rates / len(reviews)
            return round(average, 1)
        else:
            return 0.0

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
