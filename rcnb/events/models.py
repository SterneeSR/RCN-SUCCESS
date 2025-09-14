# rcnb/events/models.py
from django.db import models

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    event_date = models.DateTimeField()
    location = models.CharField(max_length=200)
    image = models.ImageField(upload_to='event_images/', blank=True, null=True)
    link = models.URLField(blank=True, help_text="Link to LinkedIn or other external page.")
    tags = models.CharField(max_length=200, blank=True, help_text="Comma-separated tags, e.g., #nanotechnology, #healthcare")
    details_pdf = models.FileField(upload_to='event_pdfs/', blank=True, null=True, help_text="Optional: Upload a PDF with more details.")

    class Meta:
        ordering = ['-event_date']

    def __str__(self):
        return self.title

    def get_tags_as_list(self):
        return [tag.strip() for tag in self.tags.split(',') if tag.strip()]