from django.contrib import admin

from products.models import Product, ProductCategory


admin.site.register(ProductCategory)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity', 'category')
    fields = ('name', 'image', 'description', 'quantity', 'price', 'category')
    search_fields = ('name',)
