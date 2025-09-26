# rcnb/products/views.py

from django.db.models import Q
from django.http import JsonResponse  # <-- Import JsonResponse
from django.shortcuts import get_object_or_404, render
from .models import Product
from favorites.models import Favorite
from startups.models import Startup
import re

def product_detail(request, slug):
    p = get_object_or_404(Product.objects.select_related("startup"), slug=slug)
    # The TemplateDoesNotExist error comes from here.
    # Make sure this template exists at:
    # rcnb/products/templates/products/product_detail.html
    return render(request, "products/product_detail.html", {"p": p})

PAGE_SIZE = 12

def product_list(request):
    q = (request.GET.get('q') or '').strip()
    sort = request.GET.get('sort')
    category = request.GET.get('category', '').strip()

    qs = Product.objects.select_related('startup').all()

    if category:
        qs = qs.filter(startup__category=category)

    if q:
        normalized_q = re.sub(r'[-\s]', '', q.lower())
        query = Q()
        query |= Q(name__icontains=q)
        query |= Q(startup__name__icontains=q)
        query |= Q(tag__icontains=q)
        query |= Q(description__icontains=q)
        query |= Q(name__icontains=q.replace(' ', '-'))
        query |= Q(name__icontains=q.replace('-', ' '))
        if len(normalized_q) >= 2:
            for product in Product.objects.all():
                normalized_name = re.sub(r'[-\s]', '', product.name.lower())
                if normalized_q in normalized_name:
                    query |= Q(pk=product.pk)
        qs = qs.filter(query)

    if sort == 'price_asc':
        qs = qs.order_by('price__isnull', 'price', '-created_at')
    elif sort == 'price_desc':
        qs = qs.order_by('price__isnull', '-price', '-created_at')
    else:
        qs = qs.order_by('-created_at')

    favorited_ids = set()
    show_profile_prompt = False

    if request.user.is_authenticated:
        favorited_ids = set(Favorite.objects.filter(user=request.user).values_list('product_id', flat=True))
        if not request.user.addresses.exists():
            show_profile_prompt = True

    used_categories = Startup.objects.exclude(category='undefined').values_list('category', flat=True).distinct()
    category_choices = [choice for choice in Startup.CATEGORY_CHOICES if choice[0] in used_categories]

    page = max(int(request.GET.get('page', '1') or 1), 1)
    start, end = (page - 1) * PAGE_SIZE, page * PAGE_SIZE

    ctx = {
        "products": list(qs[start:end]),
        "favorited_ids": favorited_ids,
        "q": q,
        "sort": sort,
        "page": page,
        "has_next": qs.count() > end,
        "categories": category_choices,
        "selected_category": category,
        "show_profile_prompt": show_profile_prompt,
    }
    return render(request, "products/product_list.html", ctx)

# --- FIX ---
# Both functions now return a valid, empty JSON response.
def product_suggest(request):
    """
    Placeholder view for product suggestions.
    """
    return JsonResponse({"suggestions": []})

# --- FIX ---
def popular_searches(request):
    """
    Placeholder view for popular searches.
    """
    return JsonResponse({"popular_searches": []})

import logging
logger = logging.getLogger(__name__)

def debug_cloudinary_upload(file):
    import cloudinary.uploader
    try:
        result = cloudinary.uploader.upload(file)
        logger.warning(f"Cloudinary Upload Success: {result.get('secure_url')}")
    except Exception as e:
        logger.error(f"Cloudinary Upload Failed: {e}")
