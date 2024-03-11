from django.db import models
from django.contrib.auth.models import User
from utils.generate_code import generate_code
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, related_name='user_profile', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_pics')
    code = models.CharField(max_length=10, default=generate_code)

    def __str__(self):
        return str(self.user)


@receiver(post_save, sender=User)
def created_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(
            user=instance,
        )


PHONE_TYPE = (
    ('Primary', 'Primary'),
    ('Secondary', 'Secondary'),
)


class ContactNumbers(models.Model):
    user = models.OneToOneField(User, related_name='user_numbers', on_delete=models.CASCADE)
    type = models.CharField(max_length=12, choices=PHONE_TYPE)
    number = models.CharField(max_length=15)

    def __str__(self):
        return str(self.user)


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
