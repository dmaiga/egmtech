# Vision produit

## Resume

Nous construisons une plateforme digitale B2B/B2C pour une entreprise specialisee dans :

- l'installation et la vente d'equipements de securite electronique ;
- l'installation et la maintenance de reseaux telecom et fibre optique ;
- les solutions d'energie solaire et centrales electriques ;
- les infrastructures reseau informatique.

Cette plateforme doit servir a la fois de vitrine technique, de canal de vente, d'outil de qualification commerciale et de backoffice de gestion.

## Pourquoi ce projet

Le besoin metier depasse largement le cadre d'une boutique en ligne classique. L'entreprise vend :

- des produits standards pouvant etre commandes rapidement ;
- des solutions techniques complexes qui necessitent qualification, chiffrage et validation ;
- des prestations de terrain liees a l'installation, la maintenance et l'integration.

La plateforme doit donc melanger logique e-commerce et logique CRM/commerciale.

## Cibles

- clients particuliers recherchant un equipement standard ;
- entreprises ayant besoin de devis ou d'accompagnement technique ;
- equipe commerciale interne ;
- administrateurs et responsables operationnels.

## Capacites attendues

### 1. Presentation structuree des solutions

Le site doit presenter clairement les domaines d'activite :

- videosurveillance ;
- alarmes intrusion ;
- controle d'acces ;
- telecom et fibre optique ;
- energie solaire ;
- reseaux informatiques.

Chaque domaine doit pouvoir exposer :

- les offres ;
- les cas d'usage ;
- les produits associes ;
- les services d'installation et maintenance ;
- les avantages techniques et commerciaux.

### 2. Vente directe de produits standards

Pour les references tenues en stock, la plateforme doit permettre :

- consultation du catalogue ;
- visualisation des fiches produit ;
- affichage du stock ou de la disponibilite ;
- achat direct ;
- suivi de commande.

### 3. Demandes de devis

Pour les projets specifiques, les besoins sur mesure ou les grandes quantites, la plateforme doit permettre :

- soumission de demandes detaillees ;
- ajout de contexte technique ;
- qualification commerciale ;
- validation interne ;
- reponse sous forme de proposition ou proforma.

### 4. Gestion des proformas commerciales

La plateforme doit integrer un mecanisme de :

- generation de proformas ;
- validation commerciale ;
- suivi des statuts ;
- conversion en commande si acceptation.

### 5. Suivi des commandes et paiements

Le systeme doit couvrir :

- suivi des commandes ;
- suivi des statuts ;
- suivi des paiements ;
- historisation des interactions commerciales.

### 6. Backoffice commercial

Le backoffice doit permettre a l'equipe interne de :

- gerer le catalogue ;
- suivre les demandes de devis ;
- valider ou convertir les opportunites ;
- mettre a jour les statuts de commande ;
- consulter les informations utiles au pilotage commercial.

## Lecture de l'existant

A ce stade, le projet Django couvre deja plusieurs briques :

- catalogue public ;
- comptes utilisateurs ;
- achat direct simple ;
- demande de devis simple sur produit ;
- historique client ;
- backoffice basique pour produits, categories et commandes.

Le projet est donc une base operationnelle de MVP, mais pas encore la plateforme commerciale complete visee.

## Ecart entre MVP actuel et cible

Les points majeurs a ajouter sont :

- modelisation des solutions metier en plus des produits ;
- demandes de devis multi-produits ou hors catalogue ;
- generation de proformas ;
- suivi de paiement ;
- gestion commerciale plus fine du pipe B2B ;
- meilleur cloisonnement des roles internes ;
- tableaux de bord et reporting.

## Proposition de trajectoire

### Phase 1. Stabilisation du socle

- fiabiliser les workflows existants ;
- renforcer les validations ;
- ajouter des tests ;
- documenter les parcours utilisateur.

### Phase 2. Cadrage B2B

- creer une entite de demande commerciale distincte de la commande ;
- supporter plusieurs lignes, commentaires et pieces jointes ;
- introduire la notion de proforma.

### Phase 3. Structuration des offres

- separer produits, solutions, services et secteurs ;
- enrichir le contenu marketing et technique ;
- faciliter la navigation par besoin metier.

### Phase 4. Pilotage commercial

- suivi des paiements ;
- reporting ;
- tableaux de bord ;
- traçabilite des actions commerciales.

## Principe directeur

La bonne lecture de ce projet est la suivante :

Ce n'est pas un simple site e-commerce, mais un outil de gestion commerciale digitalise pour une entreprise technique specialisee.
