from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Product, Brand, Review, ProductImages
from django.db.models import Q, F, Value
from django.db.models.aggregates import Count, Sum, Max, Min, Avg
# from django.views.decorators.cache import cache_page


# Create your views here.


# @cache_page(60*1)
def mydebug(request):
    # data = Product.objects.all()

    # Columns with numeric data
    # data = Product.objects.filter(price=20)
    # data = Product.objects.filter(price > 90)  # This is not valid
    # data = Product.objects.filter(price__gt = 90) # here the correct way to return all products with price greater than 90
    # data = Product.objects.filter(price__gte = 90) # greater than or equal
    # data = Product.objects.filter(price__lt = 20) # less than
    # data = Product.objects.filter(price__lte = 20) # less than or equal

    # Relation
    # data = Product.objects.filter(brand__id=3) # here when I write brand__ so now I'm in brand object(table)
    # data = Product.objects.filter(brand__id__lt=3) # here we want all products that their brand (brand id less than 5)

    # Text
    # data = Product.objects.filter(name__contains='tod') # it will return all products that their name has this text...
    # data = Product.objects.filter(name__startswith='tod')
    # data = Product.objects.filter(name__endswith='thomas')
    # data = Product.objects.filter(price__isnull=True)

    # Dates
    # data = Product.objects.filter(date_column__year=2022)
    # data = Product.objects.filter(data_column__month=2)
    # data = Product.objects.filter(data_column__day=2)

    # Complex Queries
    # data = Product.objects.filter(flag="NEW", price__gt=98)
    # data = Product.objects.filter(flag="NEW").filter(price__gt=98) # this is same of above line
    # Or another way to apply it by
    # data = Product.objects.filter(
    #     Q(flag="NEW") & # and
    #     Q(price__gt=98)
    # )
    # data = Product.objects.filter(
    #     ~ Q(flag="NEW") & # not flag = new
    #     Q(price__gt=98)
    # )
    # data = Product.objects.filter(
    #     Q(flag="NEW") | # Or
    #     Q(price__gt=98)
    # )

    # Field Reference
    # data = Product.objects.filter(quantity=F('price')) # give me all products where their quantity = their price
    # data = Product.objects.filter(quantity=F('category__id')) # where quantity = category id

    # Order
    # data = Product.objects.all().order_by('name')
    # data = Product.objects.order_by('name')
    # data = Product.objects.order_by('-name') # DES
    # data = Product.objects.order_by('-name', 'price')
    # data = Product.objects.order_by('name')[:10]
    # data = Product.objects.earliest('name') # return the first one
    # data = Product.objects.latest('name') # return the last one

    # Limit Fields
    # data = Product.objects.values('name', 'price') # to choose the columns we want
    # data = Product.objects.values_list('name', 'price') # same of above line but it return them as a tuple
    # data = Product.objects.only('name', 'price') # same of values
    # data = Product.objects.defer('description') # excludes the column we doesn't want

    # Select Related  --- very powerfull
    # data = Product.objects.select_related('brand').all() # used with ForiegnKey, one-to-one
    # data = Product.objects.select_related('brand').all() # used with many-to-many

    # Aggregation: Count, Min, Max, Sum, Avg
    # data = Product.objects.aggregate(Avg('price')) # price Average
    # data = Product.objects.aggregate(my_avg=Avg('price')) # to name it
    # data = Product.objects.aggregate(
    #     myavg=Avg('price'),
    #     mycount=Count('id')
    # )

    # Annotation
    # annotations are a way to add calculated fields to a queryset.
    # Annotations allow you to perform calculations on the data retrieved
    # from the database and include the results in the queryset
    # data = Product.objects.annotate(my_sum=Value(0))
    # data = Product.objects.annotate(price_with_tax=F('price')*1.15)

    data = Product.objects.all()

    return render(request, 'products/debug.html', {'data': data})


class ProductListView(ListView):
    model = Product
    paginate_by = 100


class ProductDetailView(DetailView):
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reviews'] = Review.objects.filter(product=self.get_object())
        context['images'] = ProductImages.objects.filter(product=self.get_object())
        context['related'] = Product.objects.filter(brand=self.get_object().brand)
        return context


class BrandListView(ListView):
    model = Brand
    paginate_by = 50
    queryset = Brand.objects.annotate(product_count=Count('product_brand'))


class BrandDetailView(ListView):
    model = Product
    template_name = 'products/brand_detail.html'
    paginate_by = 50

    def get_queryset(self):
        brand = Brand.objects.get(slug=self.kwargs['slug'])
        queryset = super().get_queryset().filter(brand=brand)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['brand'] = Brand.objects.filter(slug=self.kwargs['slug']).annotate(product_count=Count('product_brand'))[0]
        return context
