from django.contrib import admin
from .models import Product, ProductImages, Brand, Review

# Register your models here.

admin.site.register(Brand)
admin.site.register(Review)


class ProductImagesAdmin(admin.TabularInline):
    model = ProductImages


class ReviewAdmin(admin.TabularInline):
    model = Review


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImagesAdmin, ReviewAdmin]
    list_display = ('name', 'id', 'quantity')
    list_filter = ('flag', )
    search_fields = ('name', 'sku', 'id')


admin.site.register(Product, ProductAdmin)
