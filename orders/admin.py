from django.contrib import admin
from .models import Order, OrderItem,QuoteRequest

admin.site.register(QuoteRequest)

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("product", "quantity", "unit_price")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "client", "status", "total_amount", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("client__username", "client__email", "client__phone")
    inlines = [OrderItemInline]
    readonly_fields = ("total_amount", "created_at")

    ordering = ("-created_at",)

