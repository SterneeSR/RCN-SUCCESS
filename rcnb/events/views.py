from django.shortcuts import render
from .models import Event, UpcomingEvent, Update

def event_list(request):
    """
    Fetches all events, upcoming events, and updates from the database
    and renders them to the event list page.
    """
    events = Event.objects.all().order_by('-date')
    upcoming_events = UpcomingEvent.objects.all().order_by('date')
    updates = Update.objects.all().order_by('-date')

    context = {
        'events': events,
        'upcoming_events': upcoming_events,
        'updates': updates,
    }
    return render(request, 'events/event_list.html', context)