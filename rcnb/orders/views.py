from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from cart.models import Cart, CartItem
from users.models import Address
from .models import Order, OrderItem
from .forms import PaymentProofForm

@login_required
def create_order(request):
    cart = get_object_or_404(Cart, user=request.user)
    addresses = Address.objects.filter(user=request.user)
    if not cart.items.exists():
        messages.warning(request, "Your cart is empty.")
        return redirect('products:product_list')

    if request.method == 'POST':
        address_id = request.POST.get('shipping_address')
        if not address_id:
            messages.error(request, "Please select a shipping address.")
            return redirect('orders:create_order')

        selected_address = get_object_or_404(Address, id=address_id, user=request.user)
        
        # Store the selected address ID in the session to use on the next page
        request.session['selected_address_id'] = selected_address.id
        return redirect('orders:payment_page')

    # If GET request, show the address selection page
    return render(request, 'orders/select_address.html', {'addresses': addresses, 'cart': cart})

@login_required
def payment_page(request):
    cart = get_object_or_404(Cart, user=request.user)
    address_id = request.session.get('selected_address_id')

    if not address_id:
        messages.error(request, "No shipping address selected. Please select an address.")
        return redirect('orders:create_order')
    
    selected_address = get_object_or_404(Address, id=address_id, user=request.user)
    total_amount = cart.get_total_cost()

    if request.method == 'POST':
        form = PaymentProofForm(request.POST, request.FILES)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.total_amount = total_amount
            order.shipping_address = selected_address
            order.save()
            
            # Create OrderItem instances for each item in the cart
            for item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price
                )
            
            # Clear the cart
            cart.items.all().delete()
            
            # Clear the session variable
            del request.session['selected_address_id']

            return redirect('orders:order_success', order_id=order.id)
    else:
        form = PaymentProofForm()

    context = {
        'form': form,
        'total_amount': total_amount,
        'shipping_address': selected_address
    }
    return render(request, 'orders/checkout_page.html', context)

@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user).prefetch_related('items__product').order_by('-created_at')
    return render(request, 'orders/order_list.html', {'orders': orders})

@login_required
def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_success.html', {'order': order})
