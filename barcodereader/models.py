from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.utils import timezone

# Manufacturer Profile (extends Django's User model)
class ManufacturerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='manufacturer_profile')
    company_name = models.CharField(max_length=255)
    Business_licence = models.CharField(max_length=255)  # New field
    address = models.TextField()
    phone_number = models.CharField(max_length=15)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.company_name

# Product Model
class Product(models.Model):
    manufacturer = models.ForeignKey(ManufacturerProfile, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=255)
    barcode = models.CharField(max_length=100, unique=True)  # Unique barcode or QR code
    qr_code = models.CharField(max_length=100, unique=True, blank=True, null=True)  # Optional QR code
    date_of_manufacture = models.DateField()
    date_of_expiry = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

# Product Image Model (for multiple images per product)
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product_images/')  # Path where images will be stored
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.product.name}"

# Product Verification Log
class ProductVerificationLog(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='verification_logs')
    scanned_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  # Consumer who scanned
    scanned_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=True)  # True if product is genuine

    def __str__(self):
        return f"{self.product.name} - {self.scanned_at}"

# Reported Fake Products
class ReportedProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reported_products')
    reported_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  # Consumer who reported
    reported_at = models.DateTimeField(auto_now_add=True)
    reason = models.TextField()  # Reason for reporting

    def __str__(self):
        return f"{self.product.name} - {self.reported_at}"