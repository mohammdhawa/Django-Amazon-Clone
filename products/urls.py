from django.urls import path
from .views import ProductListView, ProductDetailView, BrandListView, BrandDetailView

urlpatterns = [
    path('brands/', BrandListView.as_view(), name='brand_list'),
    path('brands/<slug:slug>/', BrandDetailView.as_view(), name='brand_detail'),
    path('', ProductListView.as_view(), name='product_list'),
    path('<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),
]
