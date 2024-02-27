from django.contrib import admin
from .models import Product, ProductImages, Brand, Review

# Register your models here.

admin.site.register(Brand)


class ProductImagesAdmin(admin.TabularInline):
    model = ProductImages


class ReviewAdmin(admin.TabularInline):
    model = Review


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImagesAdmin, ReviewAdmin]


admin.site.register(Product, ProductAdmin)
