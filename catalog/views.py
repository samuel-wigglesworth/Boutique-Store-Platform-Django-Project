from django.shortcuts import get_object_or_404, render

from .models import Category, Product


def product_list_view(request):
    category_id = request.GET.get("category")
    products = Product.objects.filter(is_active=True)
    if category_id:
        products = products.filter(category_id=category_id)
    context = {
        "products": products,
        "categories": Category.objects.all(),
        "selected_category": category_id,
    }
    return render(request, "catalog/product_list.html", context)


def product_detail_view(request, pk):
    product = get_object_or_404(Product, pk=pk, is_active=True)
    return render(request, "catalog/product_detail.html", {"product": product})
from django.shortcuts import render

# Create your views here.
