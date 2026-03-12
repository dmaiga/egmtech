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

    user = request.user

    if request.method == "POST":
        form = ClientProfileForm(request.POST, instance=user)

        if form.is_valid():
            form.save()
            return redirect("accounts:client_profile")

    else:
        form = ClientProfileForm(instance=user)

    return render(
        request,
        "accounts/clients/profile.html",
        {"form": form}
    )

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

    quotes = QuoteRequest.objects.filter(client=request.user).order_by("-created_at")

    return render(
        request,
        "accounts/clients/quotes.html",
        {"quotes": quotes}
    )