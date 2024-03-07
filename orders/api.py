from rest_framework import generics
from .serializers import (OrderSerializer, OrderDetailSerializer,
                          CartSerializer, CartDetailSerializer)
from .models import Order, OrderDetail, Cart, CartDetail, Coupon
from django.contrib.auth.models import User
from products.models import Product
from settings.models import DeliveryFee
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
import datetime
from rest_framework.response import Response


class OrderListAPI(generics.ListAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()  # Define the default queryset

    def get_queryset(self):
        queryset = super().get_queryset()

        # Retrieve the user based on the username from the URL kwargs
        user = User.objects.get(username=self.kwargs['username'])

        # Filter the queryset based on the user
        queryset = queryset.filter(user=user)
        return queryset

    # def list(self, request, *args, **kwargs):
    #     queryset = super().get_queryset()
    #
    #     # Retrieve the user based on the username from the URL kwargs
    #     user = User.objects.get(username=self.kwargs['username'])
    #
    #     # Filter the queryset based on the user
    #     queryset = queryset.filter(user=user)
    #     data = OrderSerializer(queryset, many=True).data
    #     return Response({'orders': data})


class OrderDetailAPI(generics.RetrieveAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()


class ApplyCouponAPI(generics.GenericAPIView):

    def post(self, request, *args, **kwargs):
        user = User.objects.get(username=self.kwargs['username']) # Url
        coupon = get_object_or_404(Coupon, code=request.data['coupon']) # request body
        delivery_fee = DeliveryFee.objects.last().fee
        cart = Cart.objects.get(user=user, status="Inprogress")

        if coupon and coupon.quantity > 0:
            today_date = datetime.datetime.today().date()
            if coupon.start_date <= today_date <= coupon.end_date:
                coupon_value = cart.cart_total / 100 * coupon.discount
                subtotal = cart.cart_total - coupon_value
                total = subtotal + delivery_fee
                cart.coupon = coupon
                cart.total_with_coupon = subtotal
                cart.save()

                coupon.quantity -= 1
                coupon.save()

                return Response({'message': 'Coupon was applied successfully'})
            else:
                return Response({'message': 'Coupon is Invalid or Expired'})

        return Response({'message': 'Coupon not found'})
