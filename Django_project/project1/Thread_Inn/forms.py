
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Product

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Enter your username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Enter your email'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Enter your password'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Confirm your password'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email').lower()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists.")
        return email


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'image', 'category']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Enter product name', 'style': 'border-radius: 10px; padding: 10px;'}),
            'description': forms.Textarea(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Enter product description', 'style': 'border-radius: 10px; padding: 10px;'}),
            'price': forms.NumberInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Enter product price', 'style': 'border-radius: 10px; padding: 10px;'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control form-control-lg', 'style': 'border-radius: 10px; padding: 10px;'}),
            'category': forms.Select(attrs={'class': 'form-control form-control-lg', 'style': 'border-radius: 10px; padding: 10px;'}),
        }