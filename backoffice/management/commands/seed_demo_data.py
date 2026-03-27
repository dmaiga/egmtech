from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Run all seed commands in the correct order to populate demo data.'

    def handle(self, *args, **kwargs):
        seed_commands = [
            "seed_user",
            "seed_order",
            "seed_payment",
            "seed_quote",
            "seed_prospectus",
        ]

        for command in seed_commands:
            self.stdout.write(self.style.WARNING(f"Running {command}..."))
            try:
                call_command(command)
                self.stdout.write(self.style.SUCCESS(f"{command} completed successfully."))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error while running {command}: {e}"))

        self.stdout.write(self.style.SUCCESS("All demo data seeded successfully."))