from django.db import models
from django.contrib.auth.models import User
from utils.generate_code import generate_code
from django.utils import timezone
from products.models import Product
from accounts.models import Address
import datetime

# Create your models here.
OREDER_STATUS = (
    ('Recieved', 'Recieved'),
    ('Delivered', 'Delivered'),
    ('Processed', 'Processed'),
    ('Shipped', 'Shipped'),
)


class Order(models.Model):
    user = models.ForeignKey(User, related_name='order_owner', on_delete=models.SET_NULL, null=True)
    status = models.CharField(choices=OREDER_STATUS, max_length=15)
    code = models.CharField(max_length=8, default=generate_code, unique=True)
    order_time = models.DateTimeField(default=timezone.now)
    delivery_time = models.DateTimeField(null=True, blank=True)
    delivery_address = models.ForeignKey(Address, related_name='delivery_address', on_delete=models.SET_NULL, null=True, blank=True)
    coupon = models.ForeignKey('Coupon', related_name='order_coupon', on_delete=models.SET_NULL, null=True, blank=True)
    total = models.FloatField(null=True, blank=True)
    total_with_coupon = models.FloatField(null=True, blank=True)

    def save(self, *args, **kwargs):
        # Attempt to save the order
        try:
            super().save(*args, **kwargs)
        except IntegrityError:
            self.code = generate_code()
            super().save(*args, **kwargs)


class OrderDetail(models.Model):
    order = models.ForeignKey(Order, related_name='order_detail', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='orderdetail_product', on_delete=models.SET_NULL, null=True,
                                blank=True)
    quantity = models.IntegerField()
    price = models.FloatField()
    total = models.FloatField(null=True, blank=True)


CART_STATUS = (
    ('Inprogress', 'Inprogress'),
    ('Completed', 'Completed'),
)


class Cart(models.Model):
    user = models.ForeignKey(User, related_name='cart_owner', on_delete=models.SET_NULL, null=True)
    status = models.CharField(choices=CART_STATUS, max_length=15)
    coupon = models.ForeignKey('Coupon', related_name='cart_coupon', on_delete=models.SET_NULL, null=True, blank=True)
    total_with_coupon = models.FloatField(null=True, blank=True)

    def save(self, *args, **kwargs):
        # Attempt to save the order
        try:
            super().save(*args, **kwargs)
        except IntegrityError:
            self.code = generate_code()
            super().save(*args, **kwargs)


class CartDetail(models.Model):
    cart = models.ForeignKey(Cart, related_name='cart_detail', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='cartdetail_product', on_delete=models.SET_NULL, null=True,
                                blank=True)
    quantity = models.IntegerField(default=1)
    total = models.FloatField(null=True, blank=True)


class Coupon(models.Model):
    code = models.CharField(max_length=20)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField()
    quantity = models.IntegerField()
    discount = models.FloatField()

    def save(self, *args, **kwargs):
        # Set end_date to one week after start_date
        if not self.end_date:
            self.end_date = self.start_date + timedelta(days=7)
        super().save(*args, **kwargs)
