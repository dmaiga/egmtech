# orders/models.py

from django.db import models, transaction
from django.contrib.auth import get_user_model
from catalog.models import Product
from django.utils import timezone

User = get_user_model()


class Order(models.Model):

    STATUS_CHOICES = (
        ("EN_ATTENTE", "Commande reçue"),
        ("EXPEDIEE", "Expédiée / chez le livreur"),
        ("LIVREE", "Livrée et payée"),
        ("ANNULEE", "Annulée"),
    )

    client = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="orders"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="EN_ATTENTE"
    )

    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    commentaire = models.TextField(blank=True)
    admin_note = models.TextField(blank=True)

    paid_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Commande #{self.id}"

    # calcul du total
    def calculate_total(self):
        total = sum(item.quantity * item.unit_price for item in self.items.all())
        self.total_amount = total
        self.save()

    # sortie du stock quand on donne le colis au livreur
    @transaction.atomic
    def mark_as_shipped(self):

        if self.status != "EN_ATTENTE":
            return

        for item in self.items.all():
            product = item.product

            if product.stock < item.quantity:
                raise ValueError(f"Stock insuffisant pour {product.name}")


        self.status = "LIVREE"
        self.save()

    # annulation commande
    @transaction.atomic
    def cancel(self):

        if self.status == "EXPEDIEE":

            for item in self.items.all():
                product = item.product
                product.stock += item.quantity
                product.save()

        self.status = "ANNULEE"
        self.save()

    # marquer comme livrée
    def mark_as_paid(self):

        self.status = "LIVREE"
        self.paid_at = timezone.now()
        self.save()
    
    @property
    def total_paid(self):
        # Somme tous les montants liés à cette commande dans la table Payment
        return sum(payment.amount for payment in self.payments.all())

    @property
    def remaining_amount(self):
        # Montant restant à payer
        return self.total_amount - self.total_paid

    @property
    def is_fully_paid(self):
        # Vérifie si la commande est totalement réglée
        return self.total_paid >= self.total_amount
    
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

    # réponse de l'admin
    admin_response = models.TextField(blank=True)

    responded_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="quote_responses"
    )

    responded_at = models.DateTimeField(null=True, blank=True)

    # fichier proforma
    proforma_file = models.FileField(
        upload_to="proformas/",
        null=True,
        blank=True
    )

    email_sent = models.BooleanField(default=False)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="EN_ATTENTE"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Devis #{self.id} - {self.client.username}"

    @property
    def total_paid(self):
        # Somme tous les montants liés à cette commande dans la table Payment
        return sum(payment.amount for payment in self.payments.all())

