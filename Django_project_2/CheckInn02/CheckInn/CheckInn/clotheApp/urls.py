from django.contrib import admin
from django.urls import path, include
from clotheApp import views as clothe_views
from . import views

urlpatterns = [
    
    path('', clothe_views.home, name='home'),
    path('generate/', views.generate_outfit, name='generate_outfit'),
    path('cart/', views.view_cart, name='cart'),
    path('add-to-cart/<int:item_id>/', views.add_to_cart_item, name='add_to_cart_item'),
    path('add-outfit-to-cart/', views.add_outfit_to_cart, name='add_outfit_to_cart'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('clear-cart/', views.clear_cart, name='clear_cart'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
]
