from django.shortcuts import render
from .models import Startup  # Import only the Startup model
from django.db.models import Q

def startups(request):
    """
    Displays a list of startups with optional filtering by category and search query.
    """
    # Get all startups from the database
    queryset = Startup.objects.all()

    # Get the selected category and search query from the request's GET parameters
    selected_category = request.GET.get('category', '')
    query = request.GET.get('q', '').strip()

    # If a category is selected, filter the queryset
    if selected_category:
        queryset = queryset.filter(category=selected_category)
    
    # If a search query is provided, further filter the queryset
    if query:
        # Create a Q object to search in both name and description fields
        search_query = Q(name__icontains=query) | Q(description__icontains=query)
        queryset = queryset.filter(search_query)

    # Prepare the context to be passed to the template
    context = {
        'startups': queryset,
        'categories': Startup.CATEGORY_CHOICES,  # Access CATEGORY_CHOICES via the Startup model
        'selected_category': selected_category,
        'q': query,
    }

    # Render the startups.html template with the context
    return render(request, 'startups/startups.html', context)