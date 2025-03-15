from django.contrib import admin
from .models import ManufacturerProfile, Product, ProductImage, ProductVerificationLog, ReportedProduct

# Inline for Product Images
class ProductImageInline(admin.TabularInline):  # or admin.StackedInline
    model = ProductImage
    extra = 1  # Number of empty image fields to display

# Manufacturer Profile Admin
@admin.register(ManufacturerProfile)
class ManufacturerProfileAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'user', 'is_approved', 'created_at')
    list_filter = ('is_approved',)
    search_fields = ('company_name', 'user__username')

# Product Admin
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]  # Add the inline for product images
    list_display = ('name', 'manufacturer', 'barcode', 'date_of_manufacture', 'date_of_expiry', 'price')
    search_fields = ('name', 'barcode', 'manufacturer__company_name')

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
