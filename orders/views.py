from django.shortcuts import render
# from .models import Order

# Create your views here.

# def order_list(request):
#     data = Order.objects.all().order_by('price') # 1 ==> sql --> db : lazy
#
#     data = Order.objects.all() # queryset cache
#     data2 = data.filter(price__gte=30)