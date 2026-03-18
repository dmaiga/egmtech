from django.shortcuts import render, get_object_or_404
from .models import Product

from catalog.models import Product, Category

def home(request):
    # On récupère les catégories actives
    categories = Category.objects.filter(is_active=True)[:6]
    
    # Les 4 derniers produits ajoutés (Nouveautés)
    latest_products = Product.objects.filter(is_active=True).order_by('-created_at')[:4]

    # Produits en promotion (ceux qui ont un pourcentage > 0)
    # Note : Vérifie si ton modèle utilise 'promo_active' ou juste 'promo_percent > 0'
    promo_products = Product.objects.filter(
        is_active=True, 
        promo_percent__gt=0
    )[:4]

    return render(
        request,
        "catalog/home.html",
        {
            "categories": categories,
            "latest_products": latest_products,
            "promo_products": promo_products,
        }
    )


from django.db.models import Q

def product_list(request):
    # On récupère tous les produits actifs
    products = Product.objects.filter(is_active=True, category__is_active=True)
    
    # Récupération des filtres depuis l'URL
    category_slug = request.GET.get('category')
    brand_name = request.GET.get('brand')
    query = request.GET.get('q') # Pour la barre de recherche globale
    sort = request.GET.get('sort')

    # Filtre par catégorie
    if category_slug:
        products = products.filter(category__slug=category_slug)
    
    # Filtre par marque
    if brand_name:
        products = products.filter(brand=brand_name)
        
    # Recherche textuelle
    if query:
        products = products.filter(
            Q(name__icontains=query) | Q(description__icontains=query) | Q(brand__icontains=query)
        )

    # Tri
    if sort == 'price_asc':
        products = products.order_by('price')
    elif sort == 'price_desc':
        products = products.order_by('-price')
    else:
        products = products.order_by('-created_at')

    # Données pour remplir la barre latérale
    categories = Category.objects.filter(is_active=True)
    # On récupère la liste unique des marques existantes en base
    brands = Product.objects.values_list('brand', flat=True).distinct()

    return render(request, "catalog/product_list.html", {
        "products": products,
        "categories": categories,
        "brands": brands,
        "current_category": category_slug,
        "current_brand": brand_name,
    })


from django.shortcuts import render, get_object_or_404
from .models import Product

from orders.forms import CartAddProductForm 

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    
    # On initialise le formulaire d'ajout au panier
    cart_product_form = CartAddProductForm()
    
    similar_products = Product.objects.filter(
        category=product.category, 
        is_active=True
    ).exclude(id=product.id)[:4]

    return render(request, "catalog/product_detail.html", {
        "product": product,
        "similar_products": similar_products,
        "cart_product_form": cart_product_form  
    })