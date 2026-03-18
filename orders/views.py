from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.db import transaction
from catalog.models import Product
from .models import Order, OrderItem
from .forms import PurchaseForm,QuoteRequestForm
from django.shortcuts import redirect, render, get_object_or_404
from catalog.models import Product
from .cart import Cart

from django.contrib import messages

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import QuoteRequestForm



@login_required
def buy_product(request, product_slug):

    product = get_object_or_404(Product, slug=product_slug, is_active=True)

    if request.method == "POST":
        form = PurchaseForm(request.POST)

        if form.is_valid():
            quantity = form.cleaned_data["quantity"]

            if product.stock < quantity:
                form.add_error("quantity", "Stock insuffisant.")
            else:
                with transaction.atomic():
                    order = Order.objects.create(
                        client=request.user,
                        order_type="ACHAT",
                        status="EN_ATTENTE"
                    )

                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        quantity=quantity,
                        unit_price=product.price
                    )

                    order.calculate_total()

                return redirect("order_success")

    else:
        form = PurchaseForm()

    return render(request, "orders/buy_product.html", {
        "form": form,
        "product": product
    })


@login_required
def request_quote(request):

    if request.method == "POST":
        form = QuoteRequestForm(request.POST, request.FILES)

        if form.is_valid():
            quote = form.save(commit=False)
            quote.client = request.user
            quote.save()

            return redirect("order_success")

    else:
        form = QuoteRequestForm()

    return render(
        request,
        "orders/request_quote.html",
        {"form": form}
    )


@login_required
def order_success(request):
    return render(request, "orders/order_success.html")

from orders.forms import CartAddProductForm 

def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(
            product=product,
            quantity=cd['quantity'],
            override_quantity=cd['override']
        )
        messages.success(request, f"{product.name} ajouté au panier !")
    
    return redirect('cart_detail')

def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    
    cart.remove(product)
    
    # Vérifier si le panier est vide après suppression
    if not cart.cart: # Accède au dictionnaire interne du panier
        messages.info(request, "Votre panier est maintenant vide.")
        return redirect('product_list') # Redirection vers le catalogue
        
    return redirect('cart_detail')


def cart_detail(request):
    cart = Cart(request)
    return render(request, 'orders/cart_detail.html', {'cart': cart})

@login_required
def checkout(request):
    cart = Cart(request)
    if not cart:
        return redirect('product_list')

    if request.method == 'POST':
        commentaire = request.POST.get('commentaire', '')
        
        # Création de la commande
        order = Order.objects.create(
            client=request.user,
            commentaire=commentaire,
            status="EN_ATTENTE"
        )
        
        # Création des lignes de commande
        for item in cart:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                unit_price=item['price'],
                quantity=item['quantity']
            )
        
        order.calculate_total()
        cart.clear() # On vide le panier après succès
        return redirect('order_success')
        
    return render(request, 'orders/checkout.html', {'cart': cart})