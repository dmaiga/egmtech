from django.core.management.base import BaseCommand
from django.utils import timezone
from accounts.models import User
from catalog.models import Product
from orders.models import Order, OrderItem

class Command(BaseCommand):
    help = 'Seed the database with demo orders.'

    def handle(self, *args, **kwargs):
        # Fetch demo users
        demo_users = User.objects.filter(role="CLIENT")[:3]
        if not demo_users.exists():
            self.stdout.write(self.style.ERROR("No demo users found. Please seed users first."))
            return

        # Fetch demo products
        demo_products = Product.objects.filter(is_active=True)[:5]
        if not demo_products.exists():
            self.stdout.write(self.style.ERROR("No demo products found. Please add products first."))
            return

        # Create demo orders
        for user in demo_users:
            order = Order.objects.create(
                client=user,
                status="EN_ATTENTE",
                total_amount=0,
                commentaire="Commande de démonstration pour {user.username}",
                created_at=timezone.now()
            )

            total = 0
            for product in demo_products[:3]:
                quantity = 2  # Fixed quantity for demo
                item = OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity,
                    unit_price=product.price
                )
                total += item.quantity * item.unit_price

            order.total_amount = total
            order.save()

            self.stdout.write(self.style.SUCCESS(f"Order #{order.id} created for user {user.username} with total {order.total_amount}"))

        self.stdout.write(self.style.SUCCESS("Seeding orders completed."))