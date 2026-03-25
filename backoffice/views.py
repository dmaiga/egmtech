from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.text import slugify
from django.contrib import messages
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Sum, Q
from django.core.paginator import Paginator
from datetime import timedelta

from accounts.forms import AdminCustomerCreationForm
from backoffice.forms import ProductForm, CategoryForm, QuoteResponseForm
from payments.forms import OrderPaymentForm, QuotePaymentForm, DirectPaymentForm

from catalog.models import Product, Category
from payments.models import Payment
from orders.models import Order ,QuoteRequest



from django.contrib.auth import get_user_model
User = get_user_model()




@login_required
def dashboard_home(request):
    if request.user.role != "ADMIN":
        return redirect("product_list")

    # Statistiques Financières
    total_revenue = Payment.objects.aggregate(Sum('amount'))['amount__sum'] or 0
    
    context = {
        # Section Commandes
        "total_orders": Order.objects.count(),
        "pending_orders": Order.objects.filter(status="EN_ATTENTE").count(),
        "confirmed_orders": Order.objects.filter(status="CONFIRMEE").count(),
        
        "total_client": User.objects.filter(role="CLIENT").count(),
        # Section Stock
        "total_products": Product.objects.count(),
        "low_stock_products": Product.objects.filter(stock__lte=5).count(),
        
        # Section Finance
        "total_revenue": total_revenue,
        
        # Activités récentes
        "recent_orders": Order.objects.select_related('client').order_by('-created_at')[:5],
        "recent_payments": Payment.objects.order_by('-id')[:5],
    }

    return render(request, "backoffice/dashboard_home.html", context)
# --- GESTION DES CLIENTS ---

@login_required
def customer_list(request):
    """Liste des clients avec recherche"""
    search_query = request.GET.get('search', '')
    # On filtre pour n'avoir que les utilisateurs qui ne sont pas admin (ou selon votre logique de rôle)
    customers = User.objects.filter(is_staff=False).order_by('-date_joined')

    if search_query:
        customers = customers.filter(
            Q(username__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(phone__icontains=search_query)
        )

    return render(request, "backoffice/customers/customer_list.html", {
        "customers": customers,
        "search_query": search_query
    })

@login_required
def customer_detail(request, pk):
    """Vue détaillée d'un client avec son historique complet"""
    customer = get_object_or_404(User, pk=pk)
    
    # On récupère tout ce qui est lié à ce client
    orders = customer.orders.all().order_by('-created_at')
    quotes = customer.quotes.all().order_by('-created_at')
    
    # Statistiques rapides
    total_spent = orders.filter(status="LIVREE").aggregate(Sum('total_amount'))['total_amount__sum'] or 0

    return render(request, "backoffice/customers/customer_detail.html", {
        "customer": customer,
        "orders": orders,
        "quotes": quotes,
        "total_spent": total_spent
    })

from django.utils.text import slugify

@login_required
def customer_create(request):
    if request.method == "POST":
        form = AdminCustomerCreationForm(request.POST, request.FILES)
        if form.is_valid():
            customer = form.save(commit=False)
            
            # --- GÉNÉRATION AUTOMATIQUE DU USERNAME ---
            base_username = slugify(f"{customer.first_name}.{customer.last_name}")
            username = base_username
            counter = 1
            
            # Boucle pour garantir l'unicité
            while User.objects.filter(username=username).exists():
                username = f"{base_username}{counter}"
                counter += 1
            
            customer.username = username
            
            # Mot de passe par défaut
            password_provisoire = "changeMe"
            customer.set_password(password_provisoire)
            customer.save()

            # Envoi de l'email
            if form.cleaned_data.get('send_welcome_email'):
                subject = "Bienvenue chez EGM - Vos accès"
                message = f"""Bonjour {customer.first_name},
                
Félicitations ! Votre compte client a été créé avec succès sur la plateforme EGM Tech.
                
Voici vos identifiants de connexion :
--------------------------------------
Identifiant : {customer.username}
Mot de passe : {password_provisoire}
--------------------------------------
                
Vous pouvez vous connecter dès maintenant pour suivre vos devis et commandes.
Nous vous conseillons de modifier votre mot de passe lors de votre première connexion.
                
Cordialement,
L'équipe EGM Electronique"""
                
                send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [customer.email])

            messages.success(request, f"Client {customer.username} créé avec succès.")
            return redirect('customer_detail', pk=customer.pk)
    else:
        form = AdminCustomerCreationForm(initial={'role': 'CLIENT'})

    return render(request, "backoffice/customers/customer_form.html", {"form": form})

# --- GESTION DES PRODUITS ---

from django.db.models import Q
from django.core.paginator import Paginator
from catalog.models import Category, Product # Vérifiez vos imports

@login_required
def product_list(request):
    """Liste tous les équipements avec filtrage avancé"""
    if request.user.role != "ADMIN":
        return redirect("dashboard_home")

    # Initialisation du queryset
    products_list = Product.objects.all().select_related('category').order_by('-created_at')

    # --- FILTRES ---
    search_query = request.GET.get('search', '')
    brand_filter = request.GET.get('brand', '')
    category_filter = request.GET.get('category', '')

    if search_query:
        products_list = products_list.filter(
            Q(name__icontains=search_query) | 
            Q(brand__icontains=search_query)
        )

    if brand_filter:
        products_list = products_list.filter(brand__iexact=brand_filter)

    if category_filter:
        products_list = products_list.filter(category_id=category_filter)

    # --- DONNÉES POUR LES SELECTS ---
    # Récupère toutes les marques uniques existantes en base
    brands = Product.objects.values_list('brand', flat=True).distinct().order_by('brand')
    categories = Category.objects.all().order_by('name')

    # --- PAGINATION (15 par page) ---
    paginator = Paginator(products_list, 15)
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)

    return render(request, "backoffice/products/product_list.html", {
        "products": products,
        "categories": categories,
        "brands": brands,
        "search_query": search_query,
        "selected_brand": brand_filter,
        "selected_category": category_filter
    })

@login_required
def product_detail(request, pk):
    """Vue détaillée d'un produit avec ses specs techniques"""
    product = get_object_or_404(Product, pk=pk)
    return render(request, "backoffice/products/product_detail.html", {"product": product})


@login_required
def product_create(request):
    if request.user.role != "ADMIN":
        return redirect("dashboard_home")

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)

        if form.is_valid():
            product = form.save(commit=False)

            base_slug = slugify(product.name)
            slug_unique = base_slug
            counter = 1

            while Product.objects.filter(slug=slug_unique).exists():
                slug_unique = f"{base_slug}-{counter}"
                counter += 1

            product.slug = slug_unique
            product.save()

            return redirect("dashboard_home")

    else:
        form = ProductForm()

    return render(request, "backoffice/products/product_form.html", {"form": form})

 

@login_required
def product_update(request, pk):
    if request.user.role != "ADMIN":
        return redirect("dashboard_home")

    product = get_object_or_404(Product, pk=pk)

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)

        if form.is_valid():
            product = form.save(commit=False)

            # Regénérer slug si le nom change
            base_slug = slugify(product.name)
            slug_unique = base_slug
            counter = 1

            while Product.objects.filter(slug=slug_unique).exclude(pk=product.pk).exists():
                slug_unique = f"{base_slug}-{counter}"
                counter += 1

            product.slug = slug_unique
            product.save()

            return redirect("bo_product_list")

    else:
        form = ProductForm(instance=product)

    return render(request, "backoffice/products/product_form.html", {
        "form": form,
        "is_update": True
    })

@login_required
def product_toggle_active(request, pk):
    if request.user.role != "ADMIN":
        return redirect("dashboard_home")

    product = get_object_or_404(Product, pk=pk)

    product.is_active = not product.is_active
    product.save()

    return redirect("bo_product_list")


@login_required
def product_delete(request, pk):
    if request.user.role != "ADMIN":
        return redirect("dashboard_home")

    product = get_object_or_404(Product, pk=pk)

    if request.method == "POST":
        product.delete()
        return redirect("bo_product_list")

    return render(request, "backoffice/products/product_confirm_delete.html", {
        "product": product
    })

# --- GESTION DES CATEGORIES ---


@login_required
def category_list(request):
    search_query = request.GET.get('search', '')
    categories = Category.objects.all()

    if search_query:
        categories = categories.filter(
            Q(name__icontains=search_query)
        )

    # On ajoute .order_by('-id') pour avoir les plus récentes en premier
    categories = categories.order_by('name')

    return render(request, "backoffice/catalog/category_list.html", {
        "categories": categories,
        "search_query": search_query
    })


@login_required
def category_create(request):
    if request.user.role != "ADMIN":
        return redirect("dashboard_home")

    if request.method == "POST":
        form = CategoryForm(request.POST, request.FILES)

        if form.is_valid():
            category = form.save(commit=False)

            base_slug = slugify(category.name)
            slug_unique = base_slug
            counter = 1

            while Category.objects.filter(slug=slug_unique).exists():
                slug_unique = f"{base_slug}-{counter}"
                counter += 1

            category.slug = slug_unique
            category.save()

            return redirect('bo_category_list')

    else:
        form = CategoryForm()

    return render(request, "backoffice/catalog/category_form.html", {"form": form})


@login_required
def category_update(request, pk):
    if request.user.role != "ADMIN":
        return redirect("dashboard_home")

    category = get_object_or_404(Category, pk=pk)

    if request.method == "POST":
        form = CategoryForm(request.POST, request.FILES, instance=category)

        if form.is_valid():
            category = form.save(commit=False)

            base_slug = slugify(category.name)
            slug_unique = base_slug
            counter = 1

            while Category.objects.filter(slug=slug_unique).exclude(pk=category.pk).exists():
                slug_unique = f"{base_slug}-{counter}"
                counter += 1

            category.slug = slug_unique
            category.save()

            return redirect("bo_category_list")

    else:
        form = CategoryForm(instance=category)

    return render(request, "backoffice/catalog/category_form.html", {
        "form": form,
        "is_update": True
    })


@login_required
def category_toggle_active(request, pk):
    if request.user.role != "ADMIN":
        return redirect("dashboard_home")

    category = get_object_or_404(Category, pk=pk)
    category.is_active = not category.is_active
    category.save()

    return redirect("bo_category_list")

# --- GESTION DES ORDERS ---


@login_required
def bo_order_list(request):
    if request.user.role != "ADMIN":
        return redirect("dashboard_home")

    orders_list = Order.objects.all().select_related('client').order_by("-created_at")

    # --- FILTRE RECHERCHE (ID, Nom, Téléphone) ---
    search_query = request.GET.get('search', '')
    if search_query:
        orders_list = orders_list.filter(
            Q(id__icontains=search_query) | 
            Q(client__username__icontains=search_query) |
            Q(client__phone__icontains=search_query)
        )

    # --- FILTRE TEMPOREL ---
    period = request.GET.get('period', '')
    today = timezone.now().today()
    
    if period == 'today':
        orders_list = orders_list.filter(created_at__date=today)
    elif period == 'week':
        last_week = today - timedelta(days=7)
        orders_list = orders_list.filter(created_at__gte=last_week)
    elif period == 'month':
        orders_list = orders_list.filter(created_at__month=today.month, created_at__year=today.year)

    # --- PAGINATION (10 par page) ---
    paginator = Paginator(orders_list, 10)
    page_number = request.GET.get('page')
    orders = paginator.get_page(page_number)

    return render(request, "backoffice/orders/order_list.html", {
        "orders": orders,
        "search_query": search_query,
        "current_period": period
    })


@login_required
def bo_order_detail(request, pk):
    if request.user.role != "ADMIN":
        return redirect("dashboard_home")

    order = get_object_or_404(Order, pk=pk)

    return render(request, "backoffice/orders/order_detail.html", {
        "order": order
    })

@login_required
def bo_order_update_status(request, pk):
    if request.user.role != "ADMIN":
        return redirect("dashboard_home")

    order = get_object_or_404(Order, pk=pk)

    if request.method == "POST":
        new_status = request.POST.get("status")
        
        # Sécurité : l'admin ne peut choisir que ces deux-là
        if new_status in ["EXPEDIEE", "ANNULEE"]:
            order.status = new_status
            order.save()
            messages.success(request, f"La commande est maintenant : {order.get_status_display()}")
        else:
            messages.error(request, "Action non autorisée via cette interface.")

    return redirect("bo_order_detail", pk=pk)



# --- GESTION DES QUOTE ---


@login_required
def quote_list(request):
    if request.user.role != "ADMIN":
        return redirect("dashboard_home")

    # On récupère tous les devis avec le client pré-chargé (optimisation SQL)
    quotes_list = QuoteRequest.objects.select_related("client").order_by("-created_at")

    # --- LOGIQUE DE RECHERCHE ---
    search_query = request.GET.get('search', '')
    if search_query:
        quotes_list = quotes_list.filter(
            Q(id__icontains=search_query) | 
            Q(client__username__icontains=search_query) |
            Q(client__email__icontains=search_query) |
            Q(client__phone__icontains=search_query) |
            Q(subject__icontains=search_query)
        )

    # --- PAGINATION (10 par page) ---
    paginator = Paginator(quotes_list, 10)
    page_number = request.GET.get('page')
    quotes = paginator.get_page(page_number)

    return render(
        request,
        "backoffice/quotes/quote_list.html",
        {
            "quotes": quotes,
            "search_query": search_query
        }
    )

@login_required
def quote_detail(request, pk):

    quote = get_object_or_404(QuoteRequest, pk=pk)

    if request.method == "POST":

        form = QuoteResponseForm(
            request.POST,
            request.FILES,
            instance=quote
        )

        if form.is_valid():

            quote = form.save(commit=False)

            quote.responded_by = request.user
            quote.responded_at = timezone.now()

            # statut automatique
            quote.status = "PROFORMA_ENVOYEE"

            quote.save()

            send_mail(
                subject=f"Réponse à votre demande de devis : {quote.subject}",
                message=quote.admin_response,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[quote.client.email],
                fail_silently=True,
            )

            quote.email_sent = True
            quote.save()

            return redirect("bo_quote_detail", pk=quote.pk)

    else:
        form = QuoteResponseForm(instance=quote)

    return render(
        request,
        "backoffice/quotes/quote_detail.html",
        {
            "quote": quote,
            "form": form
        }
    )


@login_required
def quote_close_deal(request, pk):
    quote = get_object_or_404(QuoteRequest, pk=pk)
    # On ne clôture que si ce n'est pas déjà fait
    if quote.status != "CLOTUREE":
        quote.status = "CLOTUREE"
        quote.save()
        messages.success(request, f"Le deal pour le devis #{quote.id} a été clôturé avec succès.")
    return redirect('bo_quote_detail', pk=pk)



@login_required
def direct_payment_create(request):
    if request.method == "POST":
        form = DirectPaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.received_by = request.user
            
            try:
                payment.save() 
                return redirect("payment_list")
            except ValueError as e:
                form.add_error(None, str(e))
    else:
        form = DirectPaymentForm()

    return render(request, "backoffice/payments/payment_form.html", {"form": form})


@login_required
def order_add_payment(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == "POST":
        form = OrderPaymentForm(request.POST)
        if form.is_valid():
            try:
                # Utilise la méthode save personnalisée du formulaire
                form.save(order=order, user=request.user)
                messages.success(request, f"Paiement de {form.cleaned_data['amount']} FCFA enregistré.")
            except ValueError as e:
                messages.error(request, str(e))
    return redirect('bo_order_detail', pk=pk)

@login_required
def quote_add_payment(request, pk):
    quote = get_object_or_404(QuoteRequest, pk=pk)
    if request.method == "POST":
        form = QuotePaymentForm(request.POST)
        if form.is_valid():
            form.save(quote=quote, user=request.user)
            messages.success(request, "Paiement du devis enregistré avec succès.")
    return redirect('bo_quote_detail', pk=pk)



@login_required
def payment_list(request):
    # 1. Récupération de base avec optimisations
    queryset = Payment.objects.select_related(
            "order", "quote", "product_direct"
        ).prefetch_related(
            "order__items__product"
        ).order_by("-created_at")

    # 2. Filtres temporels
    period = request.GET.get('period')
    if period == 'today':
        queryset = queryset.filter(created_at__date=timezone.now().date())
    elif period == 'week':
        last_7_days = timezone.now() - timedelta(days=7)
        queryset = queryset.filter(created_at__gte=last_7_days)
    elif period == 'month':
        queryset = queryset.filter(created_at__month=timezone.now().month)

    # 3. Recherche (ID, Nom produit direct, Nom client via Order/Quote)
    search = request.GET.get('search')
    if search:
        queryset = queryset.filter(
            Q(id__icontains=search) | 
            Q(product_direct__name__icontains=search) |
            Q(order__client__username__icontains=search) |
            Q(quote__client__username__icontains=search)
        )

    # 4. Calcul des KPIs sur le queryset filtré

    active_payments = queryset.filter(is_cancelled=False)

    stats = {
        'total_ca': active_payments.aggregate(Sum('amount'))['amount__sum'] or 0,
        'count': active_payments.count(),
        'cash_total': active_payments.filter(method='CASH').aggregate(Sum('amount'))['amount__sum'] or 0,
        'momo_total': active_payments.filter(method='MOBILE_MONEY').aggregate(Sum('amount'))['amount__sum'] or 0,
    }

    # 5. Pagination (20 par page)
    paginator = Paginator(queryset, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "backoffice/payments/payment_list.html", {
        "payments": page_obj,
        "stats": stats,
        "current_period": period,
        "search_query": search
    })


@login_required
def payment_detail(request, pk):

    payment = get_object_or_404(Payment, pk=pk)

    remaining = None

    if payment.order:
        total_paid = sum(p.amount for p in payment.order.payments.all())
        remaining = payment.order.total_amount - total_paid

    return render(request, "backoffice/payments/payment_detail.html", {
        "payment": payment,
        "remaining": remaining
    })

@login_required
def payment_cancel(request, pk):
    payment = get_object_or_404(Payment, pk=pk)
    
    if request.method == "POST":
        reason = request.POST.get('cancel_reason', 'Non spécifié')
        payment.cancel_payment(reason=reason)
        messages.warning(request, f"Le paiement #{payment.id} a été annulé. Les stocks ont été réajustés.")
        return redirect('payment_detail', pk=payment.id)
    
    return redirect('payment_detail', pk=pk)


from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, UpdateView
from site_web.models import ContactMessage
from django.urls import reverse_lazy

# Liste des messages pour le dashboard
class AdminContactListView(LoginRequiredMixin, ListView):
    model = ContactMessage
    template_name = "backoffice/customers/contact_list.html"
    context_object_name = "message"

    def get_queryset(self):
        return ContactMessage.objects.all().order_by('-created_at')

# Vue pour mettre à jour le statut ou ajouter une note
class AdminContactDetailView(LoginRequiredMixin, UpdateView):
    model = ContactMessage
    fields = ['status', 'admin_note'] # On ne permet de modifier que le statut et la note
    template_name = "backoffice/customers/contact_detail.html"
    context_object_name = "msg"
    success_url = reverse_lazy('admin_contact_list')

    def form_valid(self, form):
        # On peut ajouter une petite notification ici
        return super().form_valid(form)