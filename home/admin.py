from django.contrib import admin
from .models import Categoty, Product


@admin.register(Categoty)
class Category(admin.ModelAdmin):
    exclude = ('slug',)

@admin.register(Product)
class Product(admin.ModelAdmin):
    exclude = ('slug',)
