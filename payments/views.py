from uuid import uuid4

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from orders.models import Order

from .forms import PaymentForm
from .models import Payment


@login_required
def payment_create_view(request, order_id):
    order = get_object_or_404(Order, id=order_id, customer=request.user)
    if hasattr(order, "payment"):
        return redirect("orders:order_list")

    if request.method == "POST":
        form = PaymentForm(request.POST)
        if form.is_valid():
            Payment.objects.create(
                order=order,
                method=form.cleaned_data["method"],
                amount=order.total_amount,
                status=Payment.STATUS_COMPLETED,
                transaction_reference=str(uuid4())[:12].upper(),
            )
            order.status = Order.STATUS_PROCESSING
            order.save(update_fields=["status"])
            return redirect("orders:order_list")
    else:
        form = PaymentForm()
    return render(request, "payments/payment_create.html", {"form": form, "order": order})
from django.shortcuts import render

# Create your views here.
