# favorites/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.conf import settings

from products.models import Product
from .models import Favorite

@require_POST
def toggle_favorite(request, product_id):
    """
    Toggle favorite for product_id.
    - If AJAX and user is anonymous => return 401 JSON {'error': 'login_required'}
    - If non-AJAX and anonymous => redirect to login with next
    """
    # detect AJAX (standard header)
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'

    if not request.user.is_authenticated:
        if is_ajax:
            return JsonResponse({'error': 'login_required'}, status=401)
        login_url = settings.LOGIN_URL or reverse('login')
        return redirect(f'{login_url}?next={request.path}')

    product = get_object_or_404(Product, id=product_id)

    favorite, created = Favorite.objects.get_or_create(user=request.user, product=product)
    if not created:
        # already existed -> remove
        favorite.delete()
        is_favorited = False
    else:
        is_favorited = True

    if is_ajax:
        return JsonResponse({'is_favorited': is_favorited})
    # fallback: redirect back to favorites or product page
    return redirect('favorites:favorites_list')


def favorites_list(request):
    """
    Show favorites page. If anonymous, show login prompt instead of redirect.
    """
    if not request.user.is_authenticated:
        return render(request, 'favorites/favorites.html', {
            'products': [],
            'favorited_ids': set(),
            'login_required': True,
        })

    products = Product.objects.filter(favorite_set__user=request.user).select_related('startup').distinct()
    favorited_ids = set(Favorite.objects.filter(user=request.user).values_list('product_id', flat=True))
    return render(request, 'favorites/favorites.html', {
        'products': products,
        'favorited_ids': favorited_ids,
        'login_required': False,
    })
