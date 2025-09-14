# rcnb/orders/forms.py
from django import forms
from .models import Order

class PaymentProofForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['payment_screenshot']
        labels = {
            'payment_screenshot': 'Upload Payment Screenshot',
        }