from rest_framework.pagination import PageNumberPagination


class BrandPagination(PageNumberPagination):
    page_size = 50
