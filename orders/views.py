from django.shortcuts import render
from .models import Order, OrderDetail, Cart, CartDetail, Coupon


# Create your views here.

def order_list(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'orders/order_list.html', {'orders': orders})


def checkout(request):
    return render(request, 'orders/checkout.html', {})


def invoice(request):
    return render(request, 'orders/invoice.html', {})