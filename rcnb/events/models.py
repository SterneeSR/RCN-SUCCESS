from django.db import models
from django.utils import timezone

class Event(models.Model):
    title = models.CharField(max_length=200)
    date = models.DateField(default=timezone.now)
    short_description = models.TextField()
    full_description = models.TextField()
    image = models.ImageField(upload_to='events/', blank=True, null=True)
    linkedin_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title

class UpcomingEvent(models.Model):
    title = models.CharField(max_length=200)
    date = models.DateField(default=timezone.now)
    short_description = models.TextField()
    full_description = models.TextField()
    image = models.ImageField(upload_to='upcoming_events/', blank=True, null=True)
    linkedin_url = models.URLField(blank=True, null=True)
    posted_on = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title

class Update(models.Model):
    title = models.CharField(max_length=200)
    date = models.DateField(default=timezone.now)
    short_description = models.TextField()
    full_description = models.TextField()
    image = models.ImageField(upload_to='updates/', blank=True, null=True)
    linkedin_url = models.URLField(blank=True, null=True)
    posted_on = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title