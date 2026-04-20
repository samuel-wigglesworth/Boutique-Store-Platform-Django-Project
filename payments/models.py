from django.db import models


class Payment(models.Model):
    METHOD_CARD = "card"
    METHOD_CASH = "cash_on_delivery"
    METHOD_BANK = "bank_transfer"

    METHOD_CHOICES = [
        (METHOD_CARD, "Card"),
        (METHOD_CASH, "Cash on Delivery"),
        (METHOD_BANK, "Bank Transfer"),
    ]

    STATUS_PENDING = "pending"
    STATUS_COMPLETED = "completed"
    STATUS_FAILED = "failed"

    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending"),
        (STATUS_COMPLETED, "Completed"),
        (STATUS_FAILED, "Failed"),
    ]

    order = models.OneToOneField("orders.Order", on_delete=models.CASCADE, related_name="payment")
    method = models.CharField(max_length=20, choices=METHOD_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    transaction_reference = models.CharField(max_length=64, blank=True)
    paid_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment for order #{self.order_id}"
