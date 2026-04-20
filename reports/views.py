from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count, Sum
from django.shortcuts import render

from orders.models import Order
from payments.models import Payment


@staff_member_required
def sales_report_view(request):
    total_orders = Order.objects.count()
    total_sales = Payment.objects.filter(status=Payment.STATUS_COMPLETED).aggregate(total=Sum("amount"))["total"] or 0
    orders_by_status = Order.objects.values("status").annotate(count=Count("id")).order_by("status")
    latest_orders = Order.objects.select_related("customer")[:10]

    context = {
        "total_orders": total_orders,
        "total_sales": total_sales,
        "orders_by_status": orders_by_status,
        "latest_orders": latest_orders,
    }
    return render(request, "reports/sales_report.html", context)
