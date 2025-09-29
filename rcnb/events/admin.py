from django.contrib import admin
from .models import Event, UpcomingEvent, Update

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'short_description')
    list_filter = ('date',)
    search_fields = ('title', 'short_description', 'full_description')

@admin.register(UpcomingEvent)
class UpcomingEventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'posted_on', 'short_description')
    list_filter = ('date', 'posted_on')
    search_fields = ('title', 'short_description', 'full_description')

@admin.register(Update)
class UpdateAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'posted_on', 'short_description')
    list_filter = ('date', 'posted_on')
    search_fields = ('title', 'short_description', 'full_description')