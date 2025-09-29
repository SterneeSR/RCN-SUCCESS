# events/views.py
from django.shortcuts import render
from .models import Event, UpcomingEvent, Update

def event_list(request):
    events = Event.objects.all()
    upcoming_events = UpcomingEvent.objects.all()
    updates = Update.objects.all()
    context = {
        'events': events,
        'upcoming_events': upcoming_events,
        'updates': updates
    }
    return render(request, 'events/event_list.html', context)