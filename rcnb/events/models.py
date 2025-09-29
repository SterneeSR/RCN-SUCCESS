from django.db import models

class Event(models.Model):
    title = models.CharField(max_length=200)
    date = models.DateField()
    short_description = models.TextField()
    full_description = models.TextField()
    image = models.ImageField(upload_to='events/')
    linkedin_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title

class UpcomingEvent(models.Model):
    title = models.CharField(max_length=200)
    date = models.DateField()
    short_description = models.TextField()
    full_description = models.TextField()
    image = models.ImageField(upload_to='upcoming_events/')
    linkedin_url = models.URLField(blank=True, null=True)
    posted_on = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title

class Update(models.Model):
    title = models.CharField(max_length=200)
    date = models.DateField()
    short_description = models.TextField()
    full_description = models.TextField()
    image = models.ImageField(upload_to='updates/')
    linkedin_url = models.URLField(blank=True, null=True)
    posted_on = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title