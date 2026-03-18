from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth import get_user_model

from orders.models import Order, QuoteRequest

from accounts.forms import ClientProfileForm


from accounts.models import User
from orders.models import Order
from orders.models import QuoteRequest



def login_view(request):
    if request.method == "POST":
        identifier = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=identifier, password=password)

        if user is not None:
            login(request, user)

            # Redirection selon le rôle
            if user.role == "ADMIN":
                return redirect("dashboard_home")
            else:
                return redirect("dashboard_client")

        else:
            messages.error(request, "Identifiants invalides.")

    return render(request, "accounts/registration/login.html")


def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Nom d'utilisateur déjà utilisé.")
        else:
            user = User.objects.create_user(
                username=username,
                email=email,
                phone=phone,
                password=password
            )
            login(request, user)
            return redirect("product_list")

    return render(request, "accounts/registration/register.html")


def logout_view(request):
    logout(request)
    return redirect("product_list")


@login_required
def dashboard_client(request):

    orders = Order.objects.filter(client=request.user)
    quotes = QuoteRequest.objects.filter(client=request.user)

    context = {
        "orders_count": orders.count(),
        "quotes_count": quotes.count(),
        "recent_orders": orders.order_by("-created_at")[:5],
        "recent_quotes": quotes.order_by("-created_at")[:5],
    }

    return render(
        request,
        "accounts/clients/dashboard.html",
        context
    )


User = get_user_model()

@login_required
def client_profile(request):
    return render(request, "accounts/clients/profile.html", {"user": request.user})

@login_required
def client_profile_edit(request):
    user = request.user
    if request.method == "POST":
        form = ClientProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profil mis à jour !")
            return redirect("client_profile")
    else:
        form = ClientProfileForm(instance=user)
    
    return render(request, "accounts/clients/profile_form.html", {"form": form})

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def password_change_custom(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            # Met à jour la session pour ne pas être déconnecté
            update_session_auth_hash(request, user)
            messages.success(request, "Votre mot de passe a été mis à jour !")
            return redirect('client_profile')
        else:
            messages.error(request, "Veuillez corriger les erreurs ci-dessous.")
    else:
        form = PasswordChangeForm(user=request.user)
    
    return render(request, "accounts/clients/password_change.html", {"form": form})

@login_required
def client_orders(request):

    orders = Order.objects.filter(client=request.user).order_by("-created_at")

    return render(
        request,
        "accounts/clients/orders.html",
        {"orders": orders}
    )

@login_required
def client_quotes(request):
    """Liste simple des devis"""
    quotes = QuoteRequest.objects.filter(client=request.user).order_by("-created_at")
    return render(request, "accounts/clients/quote_list.html", {"quotes": quotes})

@login_required
def quote_detail(request, id):
    """Page de détail d'un devis spécifique"""
    quote = get_object_or_404(QuoteRequest, id=id, client=request.user)
    return render(request, "accounts/clients/quote_detail.html", {"quote": quote})