from django.contrib import admin
from .models import ClothingItem, Cart
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin


admin.site.register(ClothingItem)
admin.site.register(Cart)
