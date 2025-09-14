from django.db import models
from django.conf import settings
from products.models import Product
from users.models import Address  # For shipping address

class Order(models.Model):
    STATUS_CHOICES = (
        ('AWAITING_VERIFICATION', 'Awaiting Verification'),
        ('PROCESSING', 'Processing'),
        ('SHIPPED', 'Shipped'),
        ('COMPLETED', 'Completed'),
        ('CANCELED', 'Canceled'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    shipping_address = models.ForeignKey(
        Address,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='orders'
    )
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_screenshot = models.ImageField(upload_to='payment_proofs/')
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='AWAITING_VERIFICATION')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} by {self.user.username} - {self.status}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"
