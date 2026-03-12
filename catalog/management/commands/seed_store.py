from django.core.management.base import BaseCommand
from catalog.models import Category, Product
from django.utils.text import slugify
import random


class Command(BaseCommand):

    help = "Seed database with categories and products"

    def handle(self, *args, **kwargs):

        categories = [
            "Caméras IP",
            "CCTV",
            "Alarmes",
            "Accessoires",
            "Contrôle d'accès",
            "Analyse vidéo",
            "Interphone vidéo",
            "Audiovisuel",
            "Réseaux",
            "Smart home",
            "Alarme incendie",
        ]

        category_objects = []

        for name in categories:
            category, created = Category.objects.get_or_create(
                name=name,
                slug=slugify(name)
            )
            category_objects.append(category)

        self.stdout.write(self.style.SUCCESS("Categories created"))

        products = [
            "Caméra Hikvision DS-2CD",
            "Caméra Dahua IPC-HDW",
            "Switch TP-Link 24 Ports",
            "Routeur Ubiquiti EdgeRouter",
            "Alarme Ajax Hub",
            "Détecteur de mouvement Bosch",
            "Contrôleur accès ZKTeco",
            "Interphone vidéo Hikvision",
            "Switch Cisco Catalyst",
            "Caméra PTZ Dahua",
            "NVR Hikvision 16 canaux",
            "Point d'accès Ubiquiti UniFi",
        ]

        for name in products:

            category = random.choice(category_objects)

            price = random.randint(50, 800)

            Product.objects.create(
                name=name,
                slug=slugify(name) + str(random.randint(1, 1000)),
                category=category,
                brand=random.choice(
                    ["Hikvision", "Dahua", "Cisco", "Ubiquiti", "Bosch", "TP-Link"]
                ),
                price=price,
                stock=random.randint(5, 100),
                promo_active=random.choice([True, False]),
                promo_percent=random.choice([0, 10, 15, 20]),
                description="Produit professionnel pour installation sécurité ou réseau."
            )

        self.stdout.write(self.style.SUCCESS("Products created"))