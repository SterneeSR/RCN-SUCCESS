# startups/views.py
from django.db.models import Q
from django.shortcuts import render
from .models import Startup

def startups_list(request):
    q = request.GET.get('q', '').strip()
    category = request.GET.get('category', 'all').strip()

    qs = Startup.objects.all()

    # Apply category filter
    if category and category != 'all':
        qs = qs.filter(category=category)

    # Apply search filter
    if q:
        qs = qs.filter(
            Q(name__icontains=q) |
            Q(description__icontains=q)
        )

    categories_list = [
        {"value": "all", "label": "All"}, # Add "All" to the list
    ] + [
        {"value": value, "label": label}
        for (value, label) in Startup.CATEGORY_CHOICES
        if value != "undefined"
    ]
    
    ctx = {
        "startups": qs, # No need for pagination here unless you're implementing it properly
        "q": q,
        "selected_category": category, # Pass the selected category back to the template
        "categories": categories_list,
    }

    return render(request, "startups/startups.html", ctx)