from django.urls import path
from .views import order_list, checkout, invoice

urlpatterns = [
    path('', order_list, name='order_list'),
    path('checkout/', checkout, name='checkout'),
    path('invoice/', invoice, name='invoice'),
]
