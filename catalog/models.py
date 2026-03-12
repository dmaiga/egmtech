#catalog/models
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to="categories/", blank=True, null=True) # Nouveau champ
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name


class Product(models.Model):

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products"
    )

    name = models.CharField(max_length=150)

    datasheet = models.FileField(upload_to="datasheets/", blank=True, null=True)

    brand = models.CharField(max_length=100, blank=True)

    slug = models.SlugField(unique=True)

    description = models.TextField(blank=True)

    price = models.DecimalField(max_digits=10, decimal_places=2)

    stock = models.PositiveIntegerField(default=0)

    image = models.ImageField(upload_to="products/", blank=True, null=True)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    # PROMOTION
    promo_percent = models.PositiveIntegerField(
        default=0,
        help_text="Réduction en pourcentage"
    )

    promo_active = models.BooleanField(default=False)

    def get_promo_price(self):

        if self.promo_active and self.promo_percent > 0:
            discount = (self.price * self.promo_percent) / 100
            return self.price - discount

        return self.price

    def __str__(self):
        return self.name
