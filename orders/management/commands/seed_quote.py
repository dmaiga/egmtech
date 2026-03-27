from django.core.management.base import BaseCommand
from django.utils import timezone
from accounts.models import User
from orders.models import QuoteRequest
from payments.models import Payment

class Command(BaseCommand):
    help = 'Seed the database with demo quote requests.'

    def handle(self, *args, **kwargs):
        # Fetch demo users
        demo_users = User.objects.filter(role="CLIENT")[:3]
        if not demo_users.exists():
            self.stdout.write(self.style.ERROR("No demo users found. Please seed users first."))
            return

        # Create demo quote requests
        statuses = ["EN_ATTENTE", "PROFORMA_ENVOYEE", "CLOTUREE"]
        for i, user in enumerate(demo_users):
            quote = QuoteRequest.objects.create(
                client=user,
                subject=f"Demande de devis {i+1}",
                description=f"Description pour la demande de devis {i+1}.",
                status=statuses[i % len(statuses)],
                created_at=timezone.now()
            )

            # Add payments for closed quotes
            if quote.status == "CLOTUREE":
                Payment.objects.create(
                    payment_type="QUOTE",
                    amount=5000,  # Example amount
                    method="BANK_TRANSFER",
                    reference=f"PAY-QUOTE-{quote.id}",
                    quote=quote,
                    received_by=user,
                    created_at=timezone.now()
                )

            self.stdout.write(self.style.SUCCESS(f"Quote #{quote.id} created for user {user.username} with status {quote.status}"))

        self.stdout.write(self.style.SUCCESS("Seeding quotes completed."))