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
from accounts.models import Address
from rest_framework import status


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

        return Response({'message': 'Coupon not found'}, status=status.HTTP_200_OK)


class CreateOrderAPI(generics.GenericAPIView):

    def post(self, request, *args, **kwargs):
        user = User.objects.get(username=self.kwargs['username'])
        code = request.data['payment_code']
        address = request.data['address_id']
        cart = Cart.objects.get(user=user, status="Inprogress")
        cart_detail = CartDetail.objects.filter(cart=cart)
        user_address = Address.objects.get(id=address)

        # cart: order | cart_detail: order detail
        new_order = Order.objects.create(
            user=user,
            status="Recieved",
            code=code,
            delivery_address=user_address,
            coupon=cart.coupon,
            total=cart.total,
            total_with_coupon=cart.total_with_coupon
        )

        # Order Detail
        for item in cart_detail:
            product = Product.objects.get(id=item.product.id)
            OrderDetail.objects.create(
                order=new_order,
                product=product,
                quantity=item.quantity,
                price=product.price,
                total=rount(item.quantity * product.price, 2)
            )

            # decrease product quantity
            product.quantity -= 1
            product.save()

        # close cart
        cart.status = "Completed"
        cart.save()

        # send email to user

        return Response({'message': 'Order was created successfully'}, status=status.HTTP_201_CREATED)


class CartCreateUpdateDeleteAPI(generics.GenericAPIView):

    def get(self, request, *args, **kwargs): # get or create
        user = User.objects.get(id=self.kwargs['username'])
        cart, created = Cart.objects.get_or_create(user=user, status="Inprogress")
        data = CartSerializer(cart).data
        return Response({'cart': data})

    def post(self, request, *args, **kwargs): # add - update
        user = User.objects.get(id=self.kwargs['username'])
        product = Product.objects.get(id=request.data['product_id'])
        quantity = int(request.data['quantity'])

        cart = Cart.objects.get(user=request.user, status='Inprogress')
        cart_detail, created = CartDetail.objects.get_or_create(cart=cart, product=product)

        cart_detail.quantity = quantity
        cart_detail.total = round(product.price * cart_detail.quantity, 2)
        cart_detail.save()

        return Response({'message': 'Cart was updated successfully'}, status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs): # delete from cart
        user = User.objects.get(id=self.kwargs['username'])
        # cart = Cart.objects.get(user=user, status="Inprogress")
        product = CartDetail.objects.get(id=request.data['item_id'])
        product.deltee()
        return Response({'message': 'Item was deleted successfully'}, status=status.HTTP_200_OK)
