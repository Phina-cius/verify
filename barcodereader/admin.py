from django.contrib import admin
from .models import ManufacturerProfile, Product, ProductImage, ProductVerificationLog, ReportedProduct, Feedback, Barcode

# Inline for Product Images
class ProductImageInline(admin.TabularInline):  # or admin.StackedInline
    model = ProductImage
    extra = 1  # Number of empty image fields to display

# Inline for Barcode
class BarcodeInline(admin.StackedInline):  # or admin.TabularInline for a more compact view
    model = Barcode
    extra = 1  # Number of empty forms to display
    can_delete = True  # Allow deletion of the barcode
    fields = ('barcode', 'qr_code')  # Fields to display in the inline form

# Manufacturer Profile Admin
@admin.register(ManufacturerProfile)
class ManufacturerProfileAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'user', 'is_approved', 'created_at')
    list_filter = ('is_approved',)
    search_fields = ('company_name', 'user__username')

# Product Admin
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline, BarcodeInline]  # Add the inlines for product images and barcode
    list_display = ('name', 'manufacturer', 'date_of_manufacture', 'date_of_expiry', 'price')
    search_fields = ('name', 'manufacturer__company_name')

# Product Image Admin
@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'image', 'uploaded_at')
    search_fields = ('product__name',)

# Product Verification Log Admin
@admin.register(ProductVerificationLog)
class ProductVerificationLogAdmin(admin.ModelAdmin):
    list_display = ('product', 'scanned_by', 'scanned_at', 'is_verified')
    list_filter = ('is_verified',)
    search_fields = ('product__name', 'scanned_by__username')

# Reported Product Admin
@admin.register(ReportedProduct)
class ReportedProductAdmin(admin.ModelAdmin):
    list_display = ('product', 'reported_by', 'reported_at')
    search_fields = ('product__name', 'reported_by__username')

# Feedback Admin
@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('name', 'message', 'created_at')
    search_fields = ('name',)

# Barcode Admin
@admin.register(Barcode)
class BarcodeAdmin(admin.ModelAdmin):
    list_display = ('barcode', 'qr_code', 'product')  # Include 'product' for clarity
    search_fields = ('barcode',)