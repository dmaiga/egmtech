from django.core.management.base import BaseCommand
from site_web.models import ContactMessage
from django.utils import timezone

class Command(BaseCommand):
    help = 'Seed the database with demo contact messages (prospectus).'

    def handle(self, *args, **kwargs):
        # Create demo contact messages
        demo_messages = [
            {
                "name": "Jean Dakouo",
                "phone": "1234567890",
                "email": "jean@example.com",
                "subject": "Demande d'informations sur les produits",
                "message": "Je souhaite en savoir plus sur vos solutions de vidéosurveillance.",
                "status": "NEW",
                "created_at": timezone.now()
            },
            {
                "name": "Abdoulaye Haidara",
                "phone": "0987654321",
                "email": "janesmith@example.com",
                "subject": "Demande de devis",
                "message": "Pouvez-vous me fournir un devis pour l'installation de panneaux solaires ?",
                "status": "IN_PROGRESS",
                "created_at": timezone.now()
            },
            {
                "name": "Abiya  Diarra",
                "phone": "1122334455",
                "email": "alicebrown@example.com",
                "subject": "Suivi de commande",
                "message": "Je souhaite avoir des informations sur le suivi de ma commande.",
                "status": "COMPLETED",
                "created_at": timezone.now()
            }
        ]

        for message_data in demo_messages:
            message, created = ContactMessage.objects.get_or_create(
                name=message_data["name"],
                phone=message_data["phone"],
                subject=message_data["subject"],
                defaults=message_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Contact message '{message.subject}' created."))
            else:
                self.stdout.write(self.style.WARNING(f"Contact message '{message.subject}' already exists."))

        self.stdout.write(self.style.SUCCESS("Seeding contact messages completed."))