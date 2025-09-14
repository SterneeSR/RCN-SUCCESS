# rcnb/events/admin.py
from django.contrib import admin
from .models import Event

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'event_date', 'location', 'details_pdf')
    list_filter = ('event_date',)
    search_fields = ('title', 'description')