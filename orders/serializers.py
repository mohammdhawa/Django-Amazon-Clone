from rest_framework import serializers
from .models import Order, OrderDetail, Cart, CartDetail, Coupon


class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDetail
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    order = OrderDetailSerializer(many=True)

    class Meta:
        model = Order
        fields = '__all__'


class CartDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartDetail
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
    cart = CartDetailSerializer(many=True)

    class Meta:
        model = Cart
        fields = '__all__'
