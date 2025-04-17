from django.db import models
from django.contrib.auth.models import AbstractUser


class ClothingItem(models.Model):
    CATEGORY_CHOICES = [
        ('upper', 'UpperWear'),
        ('lower', 'LowerWear'),
        ('shoes', 'Shoes'),
        ('accessory', 'Accessory'),
    ]
    
    COLOR_CHOICES = [
        ('red', 'Red'), ('blue', 'Blue'), ('green', 'Green'),
        ('black', 'Black'), ('white', 'White'), ('yellow', 'Yellow'), ('pink', 'Pink'),
    ]
    
    TYPE_CHOICES = [
        ('T-Shirts', 'T-Shirts'), ('Shirts', 'Shirts'), ('Jackets', 'Jackets'),('Hoodies','Hoodies'),('Sweatshirts','Sweatshirts'),
        ('Jeans', 'Jeans'), ('Trousers', 'Trousers'), ('Shorts', 'Shorts'),('Joggers',"Joggers"),('Capris','Capris'),
        ('Casual', 'Casual'), ('Boots', 'Boots'), ('Sandals', 'Sandals'),('Formal', 'Formal'),('Sports','Sports'),
        ('Hats', 'Hats'), ('Glasses','Glasses'), ('Belts', 'Belts'),('Jewelry','Jewlery'),('Watches','Watches'),
        ]

    SIZE_CHOICES = [
        ('S', 'Small'), ('M', 'Medium'), ('L', 'Large'),
        ('XL', 'X-Large'), ('XXL', 'XX-Large'),
        ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10'), ('11', '11'),  # for shoes
    ]

    STYLE_CHOICES = [
        ('Casual', 'Casual'), ('Formal', 'Formal'), ('Sports', 'Sports'),
    ]

    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)  
    size = models.CharField(max_length=10, choices=SIZE_CHOICES)
    color = models.CharField(max_length=20, choices=COLOR_CHOICES)
    style = models.CharField(max_length=50, choices=STYLE_CHOICES, blank=True) 
    image = models.ImageField(upload_to='static/images')
    price = models.IntegerField()

    def __str__(self):
        return f"{self.type} ({self.category}) - {self.color}, {self.size}"

class User(AbstractUser):
    pass

    def __str__(self):
        return self.username
    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(ClothingItem, on_delete=models.CASCADE)  
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"Cart Item:{self.product.color} {self.product.type} ({self.quantity}) :{self.product.price}"
    