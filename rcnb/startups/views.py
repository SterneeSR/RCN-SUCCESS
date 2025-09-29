# startups/views.py

from django.shortcuts import render
from .models import Startup
from django.db.models import Q
import re

def startups(request):
    # Get all startups from the database
    all_startups = Startup.objects.all()

    # Get distinct categories for the filter buttons
    categories = Startup.objects.values_list('category', flat=True).distinct()

    # Get the selected category from the request's GET parameters
    selected_category = request.GET.get('category')
    
    # Get the search query from the request's GET parameters
    q = (request.GET.get('q') or '').strip()

    if selected_category:
        # Filter startups by the selected category
        all_startups = all_startups.filter(category=selected_category)
    
    if q:
        # Further filter by the search query
        query = Q(name__icontains=q) | Q(description__icontains=q)
        all_startups = all_startups.filter(query)


    context = {
        'startups': all_startups,
        'categories': Startup.CATEGORY_CHOICES,
        'selected_category': selected_category,
        'q': q,
    }
    return render(request, 'startups/startups.html', context)