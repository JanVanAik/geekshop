import json

from django.shortcuts import render
from products.models import Product, ProductCategory


def index(request):
    context = {
        'title': 'GeekShop',
    }
    return render(request, 'products/index.html', context)


def products(request, category_id=None):
    context = {
        'title': 'GeekShop - Каталог',
        'categories': ProductCategory.objects.all(),
    }
    if category_id:
        product = Product.objects.filter(category_id=category_id)
    else:
        product = Product.objects.all()
    context['products'] = product
    return render(request, 'products/products.html', context)