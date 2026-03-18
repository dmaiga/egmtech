# payments/models.py
from django.db import models, transaction
from django.contrib.auth import get_user_model
from orders.models import Order, QuoteRequest
from catalog.models import Product
from django.utils import timezone

User = get_user_model()

class Payment(models.Model):
    TYPE_CHOICES = (
        ("ORDER", "Commande"),
        ("QUOTE", "Devis"),
        ("DIRECT", "Vente Directe / Comptant"),
    )

    METHOD_CHOICES = (
        ("CASH", "Espèces"),
        ("MOBILE_MONEY", "Mobile Money"),
        ("BANK_TRANSFER", "Virement"),
    )

    payment_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(max_length=20, choices=METHOD_CHOICES)
    reference = models.CharField(max_length=100, blank=True, help_text="ID transaction ou N° reçu")
    
    # Liaisons optionnelles selon le type
    order = models.ForeignKey(Order, null=True, blank=True, on_delete=models.SET_NULL, related_name="payments")
    quote = models.ForeignKey(QuoteRequest, null=True, blank=True, on_delete=models.SET_NULL, related_name="payments")
    
    # Pour la vente directe (si on vend un produit précis sans passer par Order)
    product_direct = models.ForeignKey(Product, null=True, blank=True, on_delete=models.SET_NULL, help_text="Uniquement pour vente directe")
    quantity_direct = models.PositiveIntegerField(default=1)

    # champs pour l'annulation
    is_cancelled = models.BooleanField(default=False)
    cancelled_at = models.DateTimeField(null=True, blank=True)
    cancel_reason = models.TextField(blank=True, null=True)

    received_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Paiement {self.id} ({self.get_payment_type_display()}) - {self.amount}"

    @transaction.atomic
    def apply_payment_logic(self):
        """
        Gère les conséquences financières et logistiques du paiement.
        """
        # --- CAS 1 : VENTE DIRECTE ---
        if self.payment_type == "DIRECT" and self.product_direct:
            if self.product_direct.stock < self.quantity_direct:
                raise ValueError(f"Stock insuffisant pour {self.product_direct.name}")
            
            self.product_direct.stock -= self.quantity_direct
            self.product_direct.save()

        # --- CAS 2 : COMMANDE (ORDER) ---
        elif self.payment_type == "ORDER" and self.order:
            # Calculer tout ce qui a été payé pour cette commande
            total_paid = sum(p.amount for p in self.order.payments.all())
            
            # Si le total payé atteint ou dépasse le montant de la commande
            if total_paid >= self.order.total_amount:
                # On ne réduit le stock que si la commande n'était pas encore traitée
                if self.order.status == "EN_ATTENTE":
                    self.order.mark_as_shipped() # Réduit le stock via votre méthode existante
                
                self.order.mark_as_paid()

        # --- CAS 3 : DEVIS (QUOTE) ---
        elif self.payment_type == "QUOTE" and self.quote:
            pass

    @transaction.atomic
    def cancel_payment(self, reason=None):
        if self.is_cancelled:
            return
        # --- 1. CAS VENTE DIRECTE ---
        if self.payment_type == "DIRECT" and self.product_direct:
            self.product_direct.stock += self.quantity_direct
            self.product_direct.save()
        # --- 2. CAS COMMANDE (ORDER) ---
        elif self.payment_type == "ORDER" and self.order:
            # On passe la commande en statut ANNULEE directement
            self.order.status = "ANNULEE"
            # IMPORTANT : On rend les produits de la commande au stock
            # On boucle sur les items de la commande pour réincrémenter le stock
            for item in self.order.items.all():
                product = item.product
                product.stock += item.quantity
                product.save()
            self.order.save()
        # --- 3. CAS DEVIS (QUOTE) ---
        elif self.payment_type == "QUOTE" and self.quote:
            # Pour un devis, on peut soit le laisser tel quel, 
            # soit le repasser en "PROFORMA_ENVOYEE" si on veut autoriser un nouveau paiement
            # Ici, on reste simple : on annule juste le flux financier
            pass
        # --- 4. MARQUAGE DU PAIEMENT ---
        self.is_cancelled = True
        self.cancelled_at = timezone.now()
        self.cancel_reason = reason
        self.save()

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new:
            self.apply_payment_logic()