from django.db import models
from taggit.managers import TaggableManager
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

# Create your models here.
FLAG_TYPES = (
    ('NEW', 'NEW'),
    ('FEATURE', 'FEATURE'),
    ('SALE', 'SALE')
)


class Product(models.Model):
    name = models.CharField(_('name'), max_length=120)
    flag = models.CharField(_('flag'), max_length=10, choices=FLAG_TYPES)
    price = models.FloatField(_('price'))
    image = models.ImageField(_('image'), upload_to='product')
    sku = models.IntegerField(_('sku'))
    subtitle = models.TextField(_('subtitle'), max_length=500)
    description = models.TextField(_('description'), max_length=50000)
    brand = models.ForeignKey('Brand', verbose_name=_('brand'), related_name='product_brand', on_delete=models.CASCADE)
    tags = TaggableManager()
    slug = models.SlugField(unique=True, null=True, blank=True)

    def save(self, *args: object, **kwargs):
        self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta: # Any query
        ordering = ('-id',)
        verbose_name = "product"
        verbose_name_plural = "products"


class ProductImages(models.Model):
    product = models.ForeignKey(Product, verbose_name=_('product'), related_name='product_images', on_delete=models.CASCADE)
    image = models.ImageField(_('image'), upload_to='product_images')


class Brand(models.Model):
    name = models.CharField(_('name'), max_length=100)
    image = models.ImageField(_('image'), upload_to='brand')
    slug = models.SlugField(unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Brand, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Review(models.Model):
    user = models.ForeignKey(User, verbose_name=_('user'), related_name='review_user', on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey(Product, verbose_name=_('product'), related_name='product_review', on_delete=models.CASCADE)
    review = models.TextField(_('review'), max_length=10000)
    rate = models.IntegerField(_('rate'), choices=[(i, i) for i in range(1, 6)])
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{str(self.product)} - {str(self.user)}"
