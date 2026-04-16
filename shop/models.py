from django.db import models
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)

    class Meta:
        verbose_name_plural = "Categories"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="In INR (₹)")
    carat = models.CharField(max_length=50, blank=True, null=True, help_text="e.g. 24K, 18K, VS1")
    weight_grams = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True, help_text="Weight in grams")
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/')
    is_primary = models.BooleanField(default=False, help_text="Set to true if this should be the main image displayed in the grid")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-is_primary', 'id']

    def save(self, *args, **kwargs):
        if self.is_primary:
            # Unset primary flag on all other images for this product
            ProductImage.objects.filter(product=self.product).exclude(pk=self.pk).update(is_primary=False)
        else:
            # If no other primary image exists for this product, force this one to be primary
            has_primary = ProductImage.objects.filter(product=self.product, is_primary=True).exclude(pk=self.pk).exists()
            if not has_primary:
                self.is_primary = True

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.title} Image"

class ContactMessage(models.Model):
    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=20)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name}"
