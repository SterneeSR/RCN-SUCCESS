# rcnb/products/views.py

import re
import cloudinary.uploader
from io import BytesIO
from PIL import Image

from django.db.models import Q
from django.core.files.storage import default_storage
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render

from .models import Product
from favorites.models import Favorite
from startups.models import Startup

PAGE_SIZE = 12


def product_list(request):
    """
    Displays a list of products with filtering, searching, sorting, and pagination.
    """
    q = (request.GET.get('q') or '').strip()
    sort = request.GET.get('sort')
    category = request.GET.get('category', '').strip()

    qs = Product.objects.select_related('startup').all()

    if category:
        qs = qs.filter(startup__category=category)

    if q:
        # Normalize query for more flexible matching
        normalized_q = re.sub(r'[-\s]', '', q.lower())
        query = Q()
        query |= Q(name__icontains=q)
        query |= Q(startup__name__icontains=q)
        query |= Q(tag__icontains=q)
        query |= Q(description__icontains=q)

        # Also match queries with different spacing/hyphenation
        query |= Q(name__icontains=q.replace(' ', '-'))
        query |= Q(name__icontains=q.replace('-', ' '))

        # Perform a deeper search if the query is long enough
        if len(normalized_q) >= 2:
            for product in Product.objects.all():
                normalized_name = re.sub(r'[-\s]', '', product.name.lower())
                if normalized_q in normalized_name:
                    query |= Q(pk=product.pk)
        qs = qs.filter(query)

    # Apply sorting options
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

    # Get categories that are actually in use
    used_categories = Startup.objects.exclude(category='undefined').values_list('category', flat=True).distinct()
    category_choices = [choice for choice in Startup.CATEGORY_CHOICES if choice[0] in used_categories]

    # Pagination logic
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


def product_detail(request, slug):
    """
    Displays the detail page for a single product.
    """
    p = get_object_or_404(Product.objects.select_related("startup"), slug=slug)
    return render(request, "products/product_detail.html", {"p": p})


def product_suggest(request):
    """
    Placeholder view for product suggestions. Returns an empty list.
    """
    return JsonResponse({"suggestions": []})


def popular_searches(request):
    """
    Placeholder view for popular searches. Returns an empty list.
    """
    return JsonResponse({"popular_searches": []})


def test_cloudinary_upload(request):
    """
    A diagnostic view to test Cloudinary uploads.
    """
    try:
        # Create a small test image in memory
        image = Image.new('RGB', (100, 100), color='red')
        buffer = BytesIO()
        image.save(buffer, format="JPEG")
        buffer.seek(0)

        # Upload the image to Cloudinary
        res = cloudinary.uploader.upload(buffer, public_id="test_upload_image")

        return JsonResponse({
            "status": "success",
            "cloudinary_url": res.get("secure_url"),
        })
    except Exception as e:
        return JsonResponse({
            "status": "error",
            "message": str(e)
        }, status=500)


def check_storage(request):
    """
    A diagnostic view to check the current default storage backend.
    """
    storage_class = default_storage.__class__.__name__
    return JsonResponse({
        "status": "success",
        "default_storage_backend": storage_class,
        "is_cloudinary": "cloudinary" in storage_class.lower()
    })