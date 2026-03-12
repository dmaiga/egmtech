#orders/models
from django.db import models
from django.contrib.auth import get_user_model
from catalog.models import Product

User = get_user_model()


class Order(models.Model):

    STATUS_CHOICES = (
        ("EN_ATTENTE", "En attente"),
        ("A_VALIDER", "À valider"),
        ("CONFIRMEE", "Confirmée"),
        ("LIVREE", "Livrée"),
        ("ANNULEE", "Annulée"),
    )

    client = models.ForeignKey(
                                User,
                                on_delete=models.CASCADE, 
                                related_name="orders")
    
    
    status = models.CharField(
            max_length=20, 
            choices=STATUS_CHOICES, 
            default="EN_ATTENTE"
            )
    
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    commentaire = models.TextField(blank=True)
    admin_note = models.TextField(blank=True)    
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def calculate_total(self):
        total = sum(item.quantity * item.unit_price for item in self.items.all())
        self.total_amount = total
        self.save()
    
    def __str__(self):
        return f"Commande #{self.id}"
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
    
class QuoteRequest(models.Model):

    STATUS_CHOICES = (
        ("EN_ATTENTE", "En attente"),
        ("PROFORMA_ENVOYEE", "Proforma envoyée"),
        ("CLOTUREE", "Clôturée"),
    )

    client = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="quotes"
    )

    subject = models.CharField(max_length=255)

    description = models.TextField()

    attachment = models.FileField(
        upload_to="quote_requests/",
        null=True,
        blank=True
    )

    proforma_file = models.FileField(
        upload_to="proformas/",
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="EN_ATTENTE"
    )

    created_at = models.DateTimeField(auto_now_add=True)