from django.contrib import admin

from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("order", "method", "amount", "status", "paid_at")
    list_filter = ("status", "method", "paid_at")
    search_fields = ("order__id", "transaction_reference")
from django.contrib import admin

# Register your models here.
