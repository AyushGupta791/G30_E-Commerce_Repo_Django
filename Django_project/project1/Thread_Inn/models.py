from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone  # Import timezone
from django.core.files.storage import FileSystemStorage



class OverwriteStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        self.delete(name)  # delete existing file
        return name

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('men', 'Men'),
        ('women', 'Women'),
        ('shoes', 'Shoes'),
        ('tshirt', 'T-Shirt'),
        ('kids', 'Kids'),
        ('bottom', 'Bottom'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    # image = models.CharField(max_length=255, blank=True, null=True)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    # image = models.ImageField(upload_to='product_images/')
    image = models.ImageField(upload_to='images/', null=True, blank=True  , storage=OverwriteStorage())
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)  # No need for default here
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.category})"



class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.product.name} (x{self.quantity})"

    def total_price(self):
        return round(self.product.price * self.quantity, 2)
