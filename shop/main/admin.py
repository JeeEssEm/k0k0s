from django.contrib import admin
from .models import Product, Order

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'mood', 'seller']
    list_filter = ['mood', 'seller']
    search_fields = ['title', 'seller']
    show_facets = admin.ShowFacets.ALWAYS

"""
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'price', 'number']
    list_filter = ['status']
    search_fields = ['title']
    show_facets = admin.ShowFacets.ALWAYS
"""