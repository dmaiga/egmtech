# Plateforme digitale commerciale B2B/B2C

Ce projet est une application Django conçue pour digitaliser l'activite commerciale d'une entreprise technique specialisee dans :

- la securite electronique : videosurveillance, alarmes, controle d'acces ;
- les reseaux telecom et la fibre optique ;
- les solutions d'energie solaire et centrales electriques ;
- les infrastructures reseau informatique.

L'objectif n'est pas de construire un simple site e-commerce. La cible produit est une plateforme commerciale hybride qui combine presentation de solutions techniques, vente de produits standards, demandes de devis, suivi commercial et administration interne.

La vision detaillee est documentee dans [docs/vision-produit.md](docs/vision-produit.md).

## Positionnement du produit

La plateforme doit permettre :

- de presenter des offres techniques structurees par domaine d'expertise ;
- de vendre en ligne des produits standards disponibles en stock ;
- de collecter des demandes de devis pour projets specifiques ou volumes importants ;
- de generer et suivre des proformas commerciales ;
- de suivre les commandes, validations et paiements ;
- d'outiller l'equipe commerciale via un backoffice.

## Etat actuel du projet

La version actuelle couvre deja un premier socle fonctionnel :

- catalogue public avec categories et fiches produits ;
- authentification avec utilisateurs `CLIENT` et `ADMIN` ;
- achat direct de produits en stock ;
- demande de devis sur produit ;
- espace client avec historique de commandes ;
- backoffice pour gerer produits, categories et statuts de commandes.

Fonctionnalites encore a construire pour atteindre la vision cible :

- presentation structuree par solutions et secteurs ;
- proformas commerciales ;
- suivi avance des paiements ;
- workflow commercial complet B2B ;
- gestion de projets techniques et demandes multi-produits ;
- reporting commercial et pilotage.

## Architecture actuelle

Le projet est organise autour de quatre applications Django :

- `accounts` : comptes utilisateurs et authentification ;
- `catalog` : categories, produits et catalogue public ;
- `orders` : achats directs, demandes de devis et historique client ;
- `backoffice` : administration commerciale et operationnelle.

## Modeles principaux

- `accounts.User` : utilisateur avec role `CLIENT` ou `ADMIN`, email et telephone uniques ;
- `catalog.Category` : categorie de produits active/inactive ;
- `catalog.Product` : produit avec marque, prix, stock, image et fiche technique ;
- `orders.Order` : commande ou demande de devis avec statut, total, commentaire et note admin ;
- `orders.OrderItem` : lignes de commande associees aux produits.

## Installation locale

Prerequis :

- Python compatible avec Django 5.2 ;
- `pip` ;
- `Pillow` pour la gestion des images produit.

Installation type :

```bash
python -m venv .venv
.venv\Scripts\activate
pip install django pillow
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## URLs principales

- `/` : catalogue public ;
- `/accounts/login/` : connexion ;
- `/accounts/register/` : inscription ;
- `/orders/my-orders/` : historique client ;
- `/dashboard/` : backoffice commercial ;
- `/admin/` : administration Django.

## Notes techniques

- Base de donnees par defaut : SQLite (`db.sqlite3`) ;
- fichiers media : `media/` ;
- utilisateur personnalise : `accounts.User` ;
- routage principal : `ecommerce/urls.py`.

## Priorites recommandees

1. Formaliser les parcours B2B : devis multi-lignes, validation commerciale et proforma.
2. Structurer le catalogue par solutions, secteurs et cas d'usage.
3. Ajouter un suivi des paiements et du cycle de vie commercial.
4. Renforcer la documentation technique et les tests applicatifs.
