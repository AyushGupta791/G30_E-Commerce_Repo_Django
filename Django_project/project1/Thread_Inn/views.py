from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from functools import wraps

from .models import Product, Cart
from .forms import ProductForm, CustomUserCreationForm

# Home View
def home(request):
    users_list = User.objects.all()
    return render(request, 'index.html', {'user': request.user, 'users_list': users_list})

# Dashboard View
@login_required
def dashboard(request):
    return render(request, "dashboard.html", {'user': request.user})

# Profile View
@login_required
def profile(request):
    return render(request, 'profile.html', {'user': request.user})

# Purchase View
def purchase(request):
    return render(request, 'purchase.html')

# Category Views
def men(request):
    products = Product.objects.filter(category='men')
    cart_items = Cart.objects.filter(user=request.user) if request.user.is_authenticated else []
    return render(request, 'men.html', {
        'products': products,
        'cart_items': cart_items,
        'total_price': total_price(request)
    })

def women(request):
    products = Product.objects.filter(category='women')
    cart_items = Cart.objects.filter(user=request.user) if request.user.is_authenticated else []
    return render(request, 'women.html', {
        'products': products,
        'cart_items': cart_items,
        'total_price': total_price(request)
    })

def bottom(request):
    products = Product.objects.filter(category='bottom')
    cart_items = Cart.objects.filter(user=request.user) if request.user.is_authenticated else []
    return render(request, 'bottom.html', {
        'products': products,
        'cart_items': cart_items,
        'total_price': total_price(request)
    })

def shoes(request):
    products = Product.objects.filter(category='shoes')
    cart_items = Cart.objects.filter(user=request.user) if request.user.is_authenticated else []
    return render(request, 'shoes.html', {
        'products': products,
        'cart_items': cart_items,
        'total_price': total_price(request)
    })

def tshirt(request):
    products = Product.objects.filter(category='tshirt')
    cart_items = Cart.objects.filter(user=request.user) if request.user.is_authenticated else []
    return render(request, 'tshirt.html', {
        'products': products,
        'cart_items': cart_items,
        'total_price': total_price(request)
    })

def kids(request):
    products = Product.objects.filter(category='kids')
    cart_items = Cart.objects.filter(user=request.user) if request.user.is_authenticated else []
    return render(request, 'kids.html', {
        'products': products,
        'cart_items': cart_items,
        'total_price': total_price(request)
    })

# Calculate Total Cart Price
def total_price(request):
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
        return sum(item.product.price * item.quantity for item in cart_items)
    return 0

# Cart View
@login_required
def cart_view(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_cost = sum(item.total_price() for item in cart_items)
    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total_cost': total_cost,
    })

# Add to Cart

@user_passes_test(lambda u: u.is_staff or u.is_superuser)
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    user = request.user
    cart_item, created = Cart.objects.get_or_create(user=user, product=product)
    if not created:
        cart_item.quantity += 1
    else:
        cart_item.quantity = 1
    cart_item.save()
    
    # Redirect to the product's category page
    return redirect(product.category)  # This assumes product.category matches your URL names

# Remove from Cart
@login_required
def remove_from_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    cart_item = Cart.objects.filter(user=request.user, product=product).first()
    
    if cart_item:
        cart_item.delete()
        messages.success(request, "Item removed from cart successfully!")
    else:
        messages.error(request, "This item is not in your cart.")
    
    return redirect('cart')

# Cart Page (View Cart)
@login_required
def cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_cost = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total_cost': total_cost
    })

# Role-based Decorator
def role_required(role):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            messages.error(request, "Role-based access is not supported currently.")
            return redirect('dashboard')
        return _wrapped_view
    return decorator

# Role Assign View (currently a placeholder)
@login_required
def role_assign(request):
    messages.warning(request, "Role assignment not supported with default User model.")
    return redirect('home')

# Admin Panel View (Restricted to Superusers)
@role_required('admin')
def admin_panel(request):
    return render(request, 'admin.html', {'user': request.user})


def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if not username or not email or not password1 or not password2:
            messages.error(request, "All fields are required.")
            return redirect('register')

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered.")
            return redirect('register')

        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()

        logout(request)
        messages.success(request, "Account created successfully! You can now log in.")
        return redirect('login')

    return render(request, 'register.html')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    form = AuthenticationForm()

    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user_obj = User.objects.get(email=email)
            user = authenticate(request, username=user_obj.username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, "Login successful!")
                return redirect('home')
            else:
                messages.error(request, "Invalid email or password.")
        except User.DoesNotExist:
            messages.error(request, "No account found with this email!")

    return render(request, 'login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect('register')


# Product Creation View (Restricted to Staff and Superadmins)
@login_required
@user_passes_test(lambda u: u.is_staff or u.is_superuser)
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Product added successfully!")
            return redirect('product_list')  # Redirect to your product list page after adding a product
    else:
        form = ProductForm()

    return render(request, 'add_product.html', {'form': form})


from django.core.exceptions import PermissionDenied

# views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Product
from django.contrib.auth.decorators import user_passes_test

def is_admin(user):
    return user.is_superuser or user.is_staff

def add_product_view(request):
    if request.method == 'POST':
        name = request.POST.get('product_name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        quantity = request.POST.get('quantity')  
        image = request.POST.get('image')  
        category = request.POST.get('category')

        if name and description and price and category:
            try:
                if image and not image.startswith("images/"):
                    image = f"images/{image}"

                Product.objects.create(
                    name=name,
                    description=description,
                    price=price,
                    image=image,
                    category=category,
                    added_by=request.user
                )
                messages.success(request, "Product added successfully!")
                return redirect('add_product')
            except Exception as e:
                messages.error(request, f"Something went wrong: {e}")
        else:
            messages.error(request, "All required fields must be filled.")

    return render(request, 'add_product.html')




# Product List View
@login_required
def product_list(request):
    if not (request.user.is_staff or request.user.is_superuser):
        raise PermissionDenied

    if request.user.is_superuser:
        products = Product.objects.all()
    else:
        products = Product.objects.filter(added_by=request.user)

    total_products = Product.objects.all().count()

    return render(request, 'product_list.html', {
        'products': products,
        'total_products': total_products,
    })



# Edit Product View
@login_required
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if not (request.user.is_superuser or (request.user.is_staff and product.added_by == request.user)):
        messages.error(request, "You don't have permission to edit this product.")
        return redirect('product_list')

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            if 'image' in request.FILES:
                product.image = request.FILES['image']
            form.save()
            messages.success(request, "Product updated successfully!")
            return redirect('product_list')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ProductForm(instance=product)

    return render(request, 'edit_product.html', {
        'form': form,
        'product': product,
        'current_image': product.image  # Pass current image to template
    })


# Delete Product View
@login_required
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if not (request.user.is_superuser or (request.user.is_staff and product.added_by == request.user)):
        raise PermissionDenied

    if request.method == 'POST':
        product.delete()
        messages.success(request, "Product deleted successfully!")
        return redirect('product_list')

    return render(request, 'confirm_delete.html', {'product': product})
