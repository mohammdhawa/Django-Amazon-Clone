from django.urls import path
from .views import ProductListView, ProductDetailView, BrandListView, BrandDetailView
from .api import ProductListAPI, ProductDetailAPI, BrandListAPI, BrandDetailAPI

urlpatterns = [
    path('brands/', BrandListView.as_view(), name='brand_list'),
    path('brands/<slug:slug>/', BrandDetailView.as_view(), name='brand_detail'),


    # API urls
    path('api/products/', ProductListAPI.as_view(), name='product_list_api'),
    path('api/products/<int:pk>/', ProductDetailAPI.as_view(), name='product_detail_api'),
    path('api/brands/', BrandListAPI.as_view(), name='brand_list_api'),
    path('api/brands/<int:pk>/', BrandDetailAPI.as_view(), name='brand_detail_api'),

    path('', ProductListView.as_view(), name='product_list'),
    path('<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),
]
