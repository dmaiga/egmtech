from django.core.management.base import BaseCommand
from accounts.models import User
from orders.models import Order
from payments.models import Payment
from django.utils import timezone

class Command(BaseCommand):
    help = 'Seed the database with demo payments.'

    def handle(self, *args, **kwargs):
        # Fetch demo orders
        demo_orders = Order.objects.filter(status="EN_ATTENTE")[:2]
        if not demo_orders.exists():
            self.stdout.write(self.style.ERROR("No demo orders found. Please seed orders first."))
            return

        # Create demo payments
        for order in demo_orders:
            payment = Payment.objects.create(
                payment_type="ORDER",
                amount=order.total_amount / 2,  # Partial payment for demo
                method="MOBILE_MONEY",
                reference=f"PAY-{order.id}",
                order=order,
                received_by=order.client,
                created_at=timezone.now()
            )

            self.stdout.write(self.style.SUCCESS(f"Payment #{payment.id} created for Order #{order.id} with amount {payment.amount}"))

        self.stdout.write(self.style.SUCCESS("Seeding payments completed."))