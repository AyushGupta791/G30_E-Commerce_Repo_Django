from django.contrib import admin
from .models import Product, Cart
from django import forms

# Customize the Product form for admin panel
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'image', 'category']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductForm  # Use the custom form
    list_display = ('name', 'category', 'price', 'image')  # Fields shown in list view
    list_filter = ('category',)
    search_fields = ('name', 'description')
    ordering = ('name',)

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'added_at')
    search_fields = ('user__username', 'product__name')
    list_filter = ('added_at',)
    ordering = ('-added_at',)
