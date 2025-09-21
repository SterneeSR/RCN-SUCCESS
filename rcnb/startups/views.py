# startups/views.py

from django.shortcuts import render
from .models import Startup

def startups(request):
    # Get all startups from the database
    all_startups = Startup.objects.all()

    # Get distinct categories for the filter buttons
    categories = Startup.objects.values_list('category', flat=True).distinct()

    # Get the selected category from the request's GET parameters
    selected_category = request.GET.get('category')

    if selected_category:
        # Filter startups by the selected category
        filtered_startups = all_startups.filter(category=selected_category)
    else:
        # If no category is selected, show all startups
        filtered_startups = all_startups

    context = {
        'startups': filtered_startups,
        'categories': categories,
        'selected_category': selected_category,
    }
    return render(request, 'startups/startups.html', context)