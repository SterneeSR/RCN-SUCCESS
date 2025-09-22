# rcnb/cart/context_processors.py
from .models import Cart
from asgiref.sync import sync_to_async

@sync_to_async
def get_cart_item_count(user):
    cart, created = Cart.objects.get_or_create(user=user)
    return cart.items.count()

async def cart_item_count(request):
    if request.user.is_authenticated:
        count = await get_cart_item_count(request.user)
        return {'cart_item_count': count}
    return {'cart_item_count': 0}