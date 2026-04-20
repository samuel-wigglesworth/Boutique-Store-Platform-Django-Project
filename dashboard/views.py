from django.db.models import Sum
from django.shortcuts import render

from catalog.models import Product
from orders.models import Order
from payments.models import Payment


def home_view(request):
    featured_products = Product.objects.filter(is_active=True)[:8]
    context = {"featured_products": featured_products}
    if request.user.is_authenticated and request.user.is_staff:
        context["admin_stats"] = {
            "products": Product.objects.count(),
            "orders": Order.objects.count(),
            "sales": Payment.objects.filter(status=Payment.STATUS_COMPLETED).aggregate(total=Sum("amount"))["total"] or 0,
        }
    return render(request, "dashboard/home.html", context)
