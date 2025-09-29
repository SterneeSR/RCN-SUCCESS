import string
import random
from django.db import models
from django.contrib.auth.models import User
from products.models import Product
from users.models import Address

def generate_unique_order_id():
    while True:
        new_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        if not Order.objects.filter(id=new_id).exists():
            return new_id

class Order(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    )

    id = models.CharField(max_length=6, primary_key=True, default=generate_unique_order_id, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_paid = models.BooleanField(default=False)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    shipping_address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    payment_screenshot = models.ImageField(upload_to='payment_proofs/', blank=True, null=True)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

    def get_status_color(self):
        return {
            'Pending': 'warning',
            'Processing': 'info',
            'Shipped': 'primary',
            'Delivered': 'success',
            'Cancelled': 'danger',
        }.get(self.status, 'secondary')


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.quantity} of {self.product.name}'

    def get_cost(self):
        return self.price * self.quantity
