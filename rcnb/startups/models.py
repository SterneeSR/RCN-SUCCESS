from django.db import models

class Startup(models.Model):
    CATEGORY_CHOICES = [
        ('undefined', 'Undefined'),
        ('health', 'Health'),
        ('food', 'Food'),
        ('sustainability', 'Environmental Sustainability'),
        ('iot_ai', 'IoT/AI'),
        ('agriculture', 'Agriculture'),
    ]

    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='startups/logos/', blank=True, null=True)  # PNG/JPEG
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='undefined')
    description = models.TextField()
    phone = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(blank=True, null=True)  # nullable
    website = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    facebook = models.URLField(blank=True)
    youtube = models.URLField(blank=True)
    info_img = models.ImageField(upload_to='startups/info/', blank=True, null=True)  # PNG/JPEG

    def __str__(self):
        return self.name
