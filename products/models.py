from django.db import models
from taggit.managers import TaggableManager
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify

# Create your models here.
FLAG_TYPES = (
    ('NEW', 'NEW'),
    ('FEATURE', 'FEATURE'),
    ('SALE', 'SALE')
)


class Product(models.Model):
    name = models.CharField(max_length=120)
    flag = models.CharField(max_length=10, choices=FLAG_TYPES)
    price = models.FloatField()
    image = models.ImageField(upload_to='product')
    sku = models.IntegerField()
    subtitle = models.TextField(max_length=500)
    description = models.TextField(max_length=50000)
    brand = models.ForeignKey('Brand', related_name='product_brand', on_delete=models.CASCADE)
    tags = TaggableManager()
    slug = models.SlugField()

    def save(self, *args: object, **kwargs):
        self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class ProductImages(models.Model):
    product = models.ForeignKey(Product, related_name='product_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images')


class Brand(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='brand')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Brand, self).save(*args, **kwargs)


class Review(models.Model):
    user = models.ForeignKey(User, related_name='sd', on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey(Product, related_name='product_review', on_delete=models.CASCADE)
    review = models.TextField(max_length=5000)
    rate = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    created_at = models.DateTimeField(default=timezone.now)
