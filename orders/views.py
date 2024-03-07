from django.shortcuts import render, redirect
from .models import Order, OrderDetail, Cart, CartDetail, Coupon
from products.models import Product
from settings.models import DeliveryFee


# Create your views here.

def order_list(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'orders/order_list.html', {'orders': orders})


def checkout(request):
    cart = Cart.objects.get(user=request.user, status="Inprogress")
    cart_detail = CartDetail.objects.filter(cart=cart)
    delivery_fee = DeliveryFee.objects.last().fee

    subtotal = cart.cart_total
    discount = 0
    total = subtotal + delivery_fee

    return render(request, 'orders/checkout.html', {
        'cart_detail': cart_detail,
        'delivery_fee': delivery_fee,
        'subtotal': subtotal,
        'discount': discount,
        'total': total,
    })


def invoice(request):
    return render(request, 'orders/invoice.html', {})


def add_to_cart(request):
    product = Product.objects.get(id=request.POST['product_id'])
    quantity = int(request.POST['quantity'])

    cart = Cart.objects.get(user=request.user, status='Inprogress')
    cart_detail, created = CartDetail.objects.get_or_create(cart=cart, product=product)

    cart_detail.quantity = quantity
    cart_detail.total = round(product.price * cart_detail.quantity, 2)
    cart_detail.save()

    return redirect('product_detail', slug=product.slug)
