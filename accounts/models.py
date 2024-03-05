from django.db import models
from django.contrib.auth.models import User


# Create your models here.
ADDRESS_TYPE = (
    ('Home', 'Home'),
    ('Office', 'Office'),
    ('Business', 'Business'),
    ('Other', 'Other'),
)


class Address(models.Model):
    user = models.OneToOneField(User, related_name='user_address', on_delete=models.CASCADE)
    address = models.TextField(max_length=100)
    address_type = models.CharField(max_length=12, choices=ADDRESS_TYPE)
