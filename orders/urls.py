from django.urls import path
from .views import order_list, checkout, invoice, add_to_cart

urlpatterns = [
    path('', order_list, name='order_list'),
    path('checkout/', checkout, name='checkout'),
    path('invoice/', invoice, name='invoice'),
    path('add_to_cart/', add_to_cart, name='add_to_cart')
]
