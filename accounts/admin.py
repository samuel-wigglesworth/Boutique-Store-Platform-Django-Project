from django.contrib import admin

from .models import CustomerProfile


@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "phone_number", "city", "country")
    search_fields = ("user__username", "user__email", "phone_number")
from django.contrib import admin

# Register your models here.
