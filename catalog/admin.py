from django.contrib import admin
from .models import Product, Order, ProductImage


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "category", "is_promo", "created_at")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name", "description")
    list_filter = ("category", "is_promo", "created_at")


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


ProductAdmin.inlines = [ProductImageInline]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "customer_name", "phone_number", "quantity", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("customer_name", "phone_number", "product__name")
