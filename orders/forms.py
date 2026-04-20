from django import forms


class AddToCartForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, initial=1)


class CheckoutForm(forms.Form):
    shipping_address = forms.CharField(widget=forms.Textarea, max_length=500)
