from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('men/', views.men, name='men'),
    path('women', views.women, name='women'),
    path('shoes', views.shoes, name='shoes'),
    path('tshirt', views.tshirt, name='tshirt'),
    path('bottom', views.bottom, name='bottom'),
    path('kids', views.kids, name='kids'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('purchase/', views.purchase, name='purchase'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('admin-panel/', views.admin_panel, name='admin_panel'),
    path('profile/', views.profile, name='profile'),
    path('role/', views.role_assign, name='role'),
    path('cart/', views.cart_view, name='cart'),
    path('add-product/', views.add_product, name='add_product'),
    path('products/', views.product_list, name='product_list'),
    path('products/<int:pk>/edit/', views.edit_product, name='edit_product'),
    path('products/<int:pk>/delete/', views.delete_product, name='delete_product'),
    path('admin-panel/', views.admin_panel, name='admin_panel'),
]







# from Thread_Inn.models import Product if not Product.objects.exists(): Product.objects.create(name="Captain America: Sam Soldier", description="Oversized T-Shirts", price=149, image="product_images/prod1_1.webp") Product.objects.create(name="Cotton Linen Stripes: Sienna", description="Cotton Linen Shirts", price=199, image="product_images/prod2_1.webp") Product.objects.create(name="Solids: Deep Sea Blue", description="Oversized T-Shirts", price=99, image="product_images/prod3.webp") Product.objects.create(name="Solids: Off White", description="Oversized T-Shirts", price=49, image="product_images/prod4.webp") Product.objects.create(name="Bloom: Ticket To Nowhere", description="Holiday Shirts", price=199, image="product_images/prod5.webp") Product.objects.create(name="Colourblock T-shirt: Varsity League", description="Oversized T-Shirts", price=99, image="product_images/prod6.webp") Product.objects.create(name="Black Panther: Wakanda Tribe", description="Oversized T-Shirts", price=89, image="product_images/prod7.webp") Product.objects.create(name="Peanuts: Keepin It Cool", description="Oversized T-Shirts", price=149, image="product_images/prod8.webp") print("Products added successfully!") else: print("Products already exist!")