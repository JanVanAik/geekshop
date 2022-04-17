from django.shortcuts import render
from django.conf import settings
from django.core.cache import cache
from products.models import Product, ProductCategory
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def index(request):
    context = {
        'title': 'GeekShop',
    }
    return render(request, 'products/index.html', context)


def get_products(category=None):
    if settings.LOW_CACHE:
        key = 'products'
        if not category is None:
            key = f'products_{category}'
        products = cache.get(key)
        if products is None:
            products = Product.objects.all().order_by('price')
            if not category is None:
                products = products.filter(category__pk=category)
            cache.set(key, products)
        return products
    if not category is None:
        return Product.object.filter(category__pk=category).order_by('price')
    return Product.object.all().order_by('price')


def products(request, category_id=None, page=1):
    if category_id:

        products = get_products(category_id)
    else:
        products = Product.objects.all()

    paginator = Paginator(products, 3)
    try:
        products_paginator = paginator.page(page)
    except PageNotAnInteger:
        products_paginator = paginator.page(1)
    except EmptyPage:
        products_paginator = paginator.page(paginator.num_pages)

    context = {
        'title': 'GeekShop - Каталог',
        'categories': ProductCategory.objects.all(),
        'products': products_paginator
    }
    return render(request, 'products/products.html', context)
