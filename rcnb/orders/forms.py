# rcnb/orders/forms.py
from django import forms
from .models import Order
from django import forms
from .models import Order
from django.core.exceptions import ValidationError

class PaymentProofForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['payment_screenshot']

    def clean_payment_screenshot(self):
        payment_screenshot = self.cleaned_data.get('payment_screenshot', False)
        if payment_screenshot:
            if payment_screenshot.size > 10 * 1024 * 1024:  # 10 MB limit
                raise ValidationError("File size is too large. Maximum size is 10 MB.")
        return payment_screenshot

class PaymentProofForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['payment_screenshot']
        labels = {
            'payment_screenshot': 'Upload Payment Screenshot',
        }