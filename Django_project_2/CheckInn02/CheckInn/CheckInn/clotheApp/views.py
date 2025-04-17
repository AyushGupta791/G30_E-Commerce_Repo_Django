from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from .forms import UserRegistrationForm, UserLoginForm
from .models import ClothingItem, Cart, User
import random

def home(request):
    return render(request, 'home.html')

def generate_outfit(request):
    price_limit = int(request.GET.get('price', 10000))

    def get_filtered_items(category, type_key, size_key, color_key, style_key=None):
        item_type = request.GET.get(type_key)
        sizes = request.GET.get(size_key, '').split(',')
        colors = request.GET.get(color_key, '').split(',')
        styles = request.GET.get(style_key, '').split(',') if style_key else []

        queryset = ClothingItem.objects.filter(category=category, price__lte=price_limit)

        if item_type:
            queryset = queryset.filter(type=item_type)

        if sizes and sizes != ['']:
            queryset = queryset.filter(size__in=sizes)

        if colors and colors != ['']:
            queryset = queryset.filter(color__in=colors)

        if style_key and styles and styles != ['']:
            queryset = queryset.filter(style__in=styles)

        return random.choice(queryset) if queryset.exists() else None

    outfit = {
        'upper': get_filtered_items('upper', 'upper_type', 'upper_sizes', 'upper_colors'),
        'lower': get_filtered_items('lower', 'lower_type', 'lower_sizes', 'lower_colors'),
        'shoes': get_filtered_items('shoes', 'shoes_type', 'shoes_sizes', 'shoes_colors'),
        'accessory': get_filtered_items('accessory', 'accessory_type', 'accessory_styles', 'accessory_colors', 'accessory_styles'),
    }

    return JsonResponse({
        cat: {
            'image': item.image.url if item else '',
            'price': item.price if item else '',
            'color': item.color if item else '',
            'id': item.id if item else '',    
        } for cat, item in outfit.items()
    })

def view_cart(request):
    cart_items = Cart.objects.all()
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    
    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }
    return render(request, 'cart.html', context)


def add_to_cart_item(request, item_id):
    if request.method == 'POST':
        item = get_object_or_404(ClothingItem, id=item_id)
        cart_item, created = Cart.objects.get_or_create(product=item)
        if not created:
            cart_item.quantity += 1
            cart_item.save()
        messages.success(request, f'{item.type} added to cart')
        return redirect('cart')
    return redirect('home')


def add_outfit_to_cart(request):
    if request.method == 'POST':
        try:
            data = request.POST
            added_items = 0
            
            if 'upper_id' in data and data['upper_id']:
                item = get_object_or_404(ClothingItem, id=data['upper_id'])
                cart_item, created = Cart.objects.get_or_create(product=item)
                if not created:
                    cart_item.quantity += 1
                    cart_item.save()
                added_items += 1
                
            if 'lower_id' in data and data['lower_id']:
                item = get_object_or_404(ClothingItem, id=data['lower_id'])
                cart_item, created = Cart.objects.get_or_create(product=item)
                if not created:
                    cart_item.quantity += 1
                    cart_item.save()
                added_items += 1
                
            if 'shoes_id' in data and data['shoes_id']:
                item = get_object_or_404(ClothingItem, id=data['shoes_id'])
                cart_item, created = Cart.objects.get_or_create(product=item)
                if not created:
                    cart_item.quantity += 1
                    cart_item.save()
                added_items += 1
                
            if 'accessory_id' in data and data['accessory_id']:
                item = get_object_or_404(ClothingItem, id=data['accessory_id'])
                cart_item, created = Cart.objects.get_or_create(product=item)
                if not created:
                    cart_item.quantity += 1
                    cart_item.save()
                added_items += 1
            
            if added_items > 0:
                messages.success(request, f'{added_items} items added to cart!')
            else:
                messages.warning(request, 'No items were added to cart. Please generate an outfit first.')
                
            return redirect('cart')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
            return redirect('home')
    return redirect('home')


def remove_from_cart(request, item_id):
    if request.method == 'POST':
        cart_item = get_object_or_404(Cart, product_id=item_id)

        if 'delete' in request.POST:
            cart_item.delete()
            messages.success(request, 'Item removed from cart')
        else:
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
                messages.success(request, 'Item quantity reduced')
            else:
                cart_item.delete()
                messages.success(request, 'Item removed from cart')
                
        return redirect('cart')
    return redirect('home')


def clear_cart(request):
    if request.method == 'POST':
        Cart.objects.all().delete()
        messages.success(request, 'Cart has been cleared')
        return redirect('cart')
    return redirect('home')

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        # Validate data
        if not all([username, email, password, confirm_password]):
            messages.error(request, 'All fields are required')
            return render(request, 'register.html')
            
        if password != confirm_password:
            messages.error(request, "Passwords don't match")
            return render(request, 'register.html')
            
        # Check if user already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return render(request, 'register.html')
            
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return render(request, 'register.html')
        
        # Create new user
        user = User(username=username, email=email, password=password)
        user.save()
        
        # Create session
        request.session['user_id'] = user.id
        messages.success(request, f'Account created for {username}!')
        return redirect('home')
        
    return render(request, 'register.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Validate data
        if not all([username, password]):
            messages.error(request, 'All fields are required')
            return render(request, 'login.html')
            
        # Check if user exists
        try:
            user = User.objects.get(username=username)
            
            # In a real app, use proper password hashing
            if user.password == password:
                # Create session
                request.session['user_id'] = user.id
                messages.success(request, f'Welcome back, {username}!')
                return redirect('home')
            else:
                messages.error(request, 'Invalid password')
        except User.DoesNotExist:
            messages.error(request, 'Username does not exist')
            
    return render(request, 'login.html')

def user_logout(request):
    if 'user_id' in request.session:
        del request.session['user_id']
    messages.success(request, 'You have been logged out')
    return redirect('home')

# Custom middleware to add user to context
class UserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.user = None
        request.user_authenticated = False
        
        if 'user_id' in request.session:
            try:
                user = User.objects.get(id=request.session['user_id'])
                request.user = user
                request.user_authenticated = True
            except User.DoesNotExist:
                pass
                
        response = self.get_response(request)
        return response


def login_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if 'user_id' not in request.session:
            messages.warning(request, 'Please log in to access this page.')
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return _wrapped_view