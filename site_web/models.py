from django.db import models

class ContactMessage(models.Model):
    STATUS_CHOICES = [
        ('NEW', 'Nouveau'),
        ('IN_PROGRESS', 'En cours'),
        ('COMPLETED', 'Traité'),
    ]

    name = models.CharField("Nom complet", max_length=100)
    phone = models.CharField("Numéro de Téléphone", max_length=20) # Crucial pour le suivi
    email = models.EmailField("Email", blank=True, null=True) # Optionnel
    subject = models.CharField("Sujet", max_length=200)
    message = models.TextField("Message")
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='NEW')
    created_at = models.DateTimeField(auto_now_add=True)
    admin_note = models.TextField("Notes de suivi", blank=True)

    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
            # Ceci définit ce qui sera affiché dans le template ou l'admin
            return f"{self.name} - {self.subject}"
