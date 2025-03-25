# the auther name: phinacius wafula simiyu
# the auther email: phinaciussimiyu143@gmail.com
# the auther phone number: +254798681812




from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.utils import timezone
import os
from django.core.files import File
from io import BytesIO
import barcode
from barcode.writer import ImageWriter
import qrcode




# Manufacturer Profile (extends Django's User model)
class ManufacturerProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='manufacturer_profile')
    company_name = models.CharField(max_length=255)
    Business_licence = models.CharField(max_length=255)  # New field
    address = models.TextField()
    phone_number = models.CharField(max_length=15)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.company_name

class Product(models.Model):
    manufacturer = models.ForeignKey(ManufacturerProfile, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=255)
    date_of_manufacture = models.DateField()
    date_of_expiry = models.DateField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Barcode(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='barcode')
    barcode = models.CharField(max_length=100, unique=True, null=True, blank=True)
    qr_code = models.CharField(max_length=100, unique=True, blank=True, null=True)
    barcode_image = models.ImageField(upload_to='barcodes/', blank=True, null=True)
    qr_code_image = models.ImageField(upload_to='qrcodes/', blank=True, null=True)

    def __str__(self):
        return f"Barcode for {self.product.name}"

    def generate_barcode(self):
        """Generate a barcode image and save it to the barcode_image field."""
        if not self.barcode:
            return

        # Generate barcode
        barcode_class = barcode.get_barcode_class('code128')
        barcode_instance = barcode_class(self.barcode, writer=ImageWriter())

        # Save barcode to a BytesIO buffer
        buffer = BytesIO()
        barcode_instance.write(buffer)
        buffer.seek(0)

        # Save the barcode image to the barcode_image field
        filename = f'barcode_{self.product.id}.png'
        self.barcode_image.save(filename, File(buffer), save=False)

    def generate_qr_code(self):
        """Generate a QR code image and save it to the qr_code_image field."""
        if not self.qr_code:
            return

        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(self.qr_code)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        # Save QR code to a BytesIO buffer
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)

        # Save the QR code image to the qr_code_image field
        filename = f'qrcode_{self.product.id}.png'
        self.qr_code_image.save(filename, File(buffer), save=False)

    def save(self, *args, **kwargs):
        """Override the save method to generate barcode and QR code images."""
        if not self.barcode_image and self.barcode:
            self.generate_barcode()
        if not self.qr_code_image and self.qr_code:
            self.generate_qr_code()
        super().save(*args, **kwargs)


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

class Feedback(models.Model):
    name=models.CharField(max_length=255)
    message=models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name



#this is the table for the counterfait product that are reported
class Counterfeit_report(models.Model):
    code = models.CharField(max_length=100,  blank=True, null=True)
    reported_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return qrcode