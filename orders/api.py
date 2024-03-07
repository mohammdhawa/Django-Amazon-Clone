from rest_framework import generics
from .serializers import (OrderSerializer, OrderDetailSerializer,
                          CartSerializer, CartDetailSerializer)
from .models import Order, OrderDetail, Cart, CartDetail, Coupon
from django.contrib.auth.models import User
from products.models import Product
from settings.models import DeliveryFee
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