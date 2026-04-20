from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from catalog.models import Product

from .forms import AddToCartForm, CheckoutForm
from .models import Order, OrderItem


def _get_cart(request):
    return request.session.setdefault("cart", {})


def _build_cart_items(cart):
    products = Product.objects.filter(id__in=cart.keys(), is_active=True)
    product_map = {str(product.id): product for product in products}
    cart_items = []
    for product_id, quantity in cart.items():
        product = product_map.get(str(product_id))
        if not product:
            continue
        cart_items.append(
            {
                "product": product,
                "quantity": quantity,
                "line_total": product.price * quantity,
            }
        )
    return cart_items


def add_to_cart_view(request, product_id):
    product = get_object_or_404(Product, id=product_id, is_active=True)
    form = AddToCartForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        cart = _get_cart(request)
        product_key = str(product.id)
        cart[product_key] = cart.get(product_key, 0) + form.cleaned_data["quantity"]
        request.session.modified = True
        return redirect("orders:cart")
    return render(request, "orders/add_to_cart.html", {"product": product, "form": form})


def cart_view(request):
    cart = _get_cart(request)
    cart_items = _build_cart_items(cart)
    total = sum(item["line_total"] for item in cart_items)
    return render(request, "orders/cart.html", {"cart_items": cart_items, "total": total})


def remove_from_cart_view(request, product_id):
    cart = _get_cart(request)
    cart.pop(str(product_id), None)
    request.session.modified = True
    return redirect("orders:cart")


@login_required
def checkout_view(request):
    cart = _get_cart(request)
    cart_items = _build_cart_items(cart)
    if not cart_items:
        return redirect("catalog:product_list")
    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = Order.objects.create(
                customer=request.user,
                shipping_address=form.cleaned_data["shipping_address"],
            )
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item["product"],
                    quantity=item["quantity"],
                    unit_price=item["product"].price,
                )
                item["product"].stock = max(item["product"].stock - item["quantity"], 0)
                item["product"].save(update_fields=["stock"])
            request.session["cart"] = {}
            request.session.modified = True
            return redirect("payments:payment_create", order_id=order.id)
    else:
        form = CheckoutForm()
    total = sum(item["line_total"] for item in cart_items)
    return render(request, "orders/checkout.html", {"form": form, "cart_items": cart_items, "total": total})


@login_required
def order_list_view(request):
    if request.user.is_staff:
        orders = Order.objects.all()
    else:
        orders = Order.objects.filter(customer=request.user)
    return render(request, "orders/order_list.html", {"orders": orders})
from django.shortcuts import render

# Create your views here.
