from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):

    list_display = (
        "order",
        "amount",
        "method",
        "reference",
        "received_by",
        "created_at",
    )

    search_fields = ("order__id", "reference")