from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from catalog.models import Product, Category
from orders.models import Order 

from backoffice.forms import ProductForm, CategoryForm

from django.utils.text import slugify

from orders.models import Order
from catalog.models import Product, Category

@login_required
def dashboard_home(request):

    if request.user.role != "ADMIN":
        return redirect("product_list")

    context = {
        "total_orders": Order.objects.count(),
        "pending_orders": Order.objects.filter(status="EN_ATTENTE").count(),
        "confirmed_orders": Order.objects.filter(status="CONFIRMEE").count(),
        "total_products": Product.objects.count(),
        "active_products": Product.objects.filter(is_active=True).count(),
        "total_categories": Category.objects.count(),
    }

    return render(request, "backoffice/dashboard_home.html", context)

# --- GESTION DES PRODUITS ---

@login_required
def product_list(request):
    """Liste tous les équipements de sécurité/télécom"""
    products = Product.objects.all().order_by('-created_at')
    return render(request, "backoffice/products/product_list.html", {"products": products})

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
    categories = Category.objects.all()
    return render(request, "backoffice/catalog/category_list.html", {"categories": categories})

@login_required
def category_create(request):
    if request.user.role != "ADMIN":
        return redirect("dashboard_home")

    if request.method == "POST":
        form = CategoryForm(request.POST)

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
        form = CategoryForm(request.POST, instance=category)

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

    orders = Order.objects.all().order_by("-created_at")

    return render(request, "backoffice/orders/order_list.html", {
        "orders": orders
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

        if new_status in dict(Order.STATUS_CHOICES):
            order.status = new_status
            order.save()
        
        if new_status == "CONFIRMEE":
            for item in order.items.all():
                item.product.stock -= item.quantity
                item.product.save()
        return redirect("bo_order_detail", pk=order.pk)
