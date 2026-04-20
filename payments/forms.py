from django import forms

from .models import Payment


class PaymentForm(forms.Form):
    method = forms.ChoiceField(choices=Payment.METHOD_CHOICES)
