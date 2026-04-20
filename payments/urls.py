from django.urls import path

from . import views

app_name = "payments"

urlpatterns = [
    path("create/<int:order_id>/", views.payment_create_view, name="payment_create"),
]
