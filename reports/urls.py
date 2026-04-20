from django.urls import path

from .views import sales_report_view

app_name = "reports"

urlpatterns = [
    path("", sales_report_view, name="sales_report"),
]
