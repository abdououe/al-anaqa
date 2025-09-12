from django.db import models
from django.utils.text import slugify
import os
import uuid


def _safe_name(original: str) -> str:
    name, ext = os.path.splitext(original)
    base = slugify(name) or "image"
    return f"{base}-{uuid.uuid4().hex[:8]}{ext.lower()}"


def product_upload_to(instance, filename: str) -> str:
    return os.path.join('products', _safe_name(filename))


def product_gallery_upload_to(instance, filename: str) -> str:
    return os.path.join('products', 'gallery', _safe_name(filename))


class Product(models.Model):
    CATEGORY_COFFRET = 'coffret'
    CATEGORY_BOITE_SIMPLE = 'boite_simple'
    CATEGORY_WALLETS = 'wallets'
    CATEGORY_PACKS = 'packs'
    CATEGORY_CHOICES = [
        (CATEGORY_COFFRET, 'Montre avec coffret'),
        (CATEGORY_BOITE_SIMPLE, 'Montre avec boîte simple'),
        (CATEGORY_WALLETS, 'Wallets'),
        (CATEGORY_PACKS, 'Packs'),
    ]

    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to=product_upload_to)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default=CATEGORY_COFFRET)
    is_promo = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Order(models.Model):
    STATUS_NEW = 'new'
    STATUS_CONFIRMED = 'confirmed'
    STATUS_CANCELLED = 'cancelled'
    STATUS_CHOICES = [
        (STATUS_NEW, 'Nouveau'),
        (STATUS_CONFIRMED, 'Confirmé'),
        (STATUS_CANCELLED, 'Annulé'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='orders')
    customer_name = models.CharField(max_length=120)
    phone_number = models.CharField(max_length=30)
    address = models.TextField()
    quantity = models.PositiveIntegerField(default=1)
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_NEW)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self) -> str:
        return f"Commande #{self.id} - {self.product.name} ({self.customer_name})"


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=product_gallery_upload_to)
    alt_text = models.CharField(max_length=200, blank=True)
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-is_primary', 'id']

    def __str__(self) -> str:
        return f"Image de {self.product.name}"
