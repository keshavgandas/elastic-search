from django.contrib import admin
from .models import Product

# Register your models here.

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'brand', 'price']
    search_fields = ['product_name', 'brand']
    list_filter = ['brand']
    list_per_page = 10
