from django.contrib import admin
from django.utils.html import format_html
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'quantity', 'price')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_amount', 'status', 'created_at', 'display_screenshot')
    list_filter = ('status', 'created_at')
    list_editable = ('status',)
    search_fields = ('user__username', 'id')
    inlines = [OrderItemInline]

    def total_amount(self, obj):
        """Calculates the total amount from related order items."""
        # Note: This assumes the related_name on your OrderItem's ForeignKey
        # to Order is 'items'. If not, use 'orderitem_set'.
        return sum(item.quantity * item.price for item in obj.items.all())
    total_amount.short_description = 'Total Amount' # Sets the column header in the admin

    def display_screenshot(self, obj):
        if obj.payment_screenshot:
            return format_html('<a href="{0}" target="_blank"><img src="{0}" width="100" /></a>', obj.payment_screenshot.url)
        return "No Screenshot"
    display_screenshot.short_description = 'Payment Proof'