from django.core.management.base import BaseCommand
from accounts.models import User

class Command(BaseCommand):
    help = 'Seed the database with demo users and an admin user.'

    def handle(self, *args, **kwargs):
        # Create demo users
        demo_users = [
            {"username": "demo_user1", "email": "demo1@example.com", "phone": "1234567890", "role": "CLIENT"},
            {"username": "demo_user2", "email": "demo2@example.com", "phone": "1234567891", "role": "CLIENT"},
            {"username": "demo_user3", "email": "demo3@example.com", "phone": "1234567892", "role": "CLIENT"},
        ]

        for user_data in demo_users:
            user, created = User.objects.get_or_create(username=user_data["username"], defaults=user_data)
            if created:
                user.set_password("pass123")
                user.save(update_fields=["password"])
                self.stdout.write(self.style.SUCCESS(f"Demo user '{user.username}' created."))
            else:
                self.stdout.write(self.style.WARNING(f"Demo user '{user.username}' already exists."))

        # Create admin user
        admin_data = {"username": "admin", "email": "admin@example.com", "phone": "1234567899", "role": "ADMIN", "is_staff": True, "is_superuser": True}
        admin_user, created = User.objects.get_or_create(username=admin_data["username"], defaults=admin_data)
        if created:
            admin_user.set_password("pass123")
            admin_user.save(update_fields=["password"])
            self.stdout.write(self.style.SUCCESS(f"Admin user '{admin_user.username}' created."))
        else:
            self.stdout.write(self.style.WARNING(f"Admin user '{admin_user.username}' already exists."))

        self.stdout.write(self.style.SUCCESS("Seeding completed."))
