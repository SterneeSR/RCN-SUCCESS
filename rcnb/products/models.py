from django.db import models
from startups.models import Startup
from django.utils.text import slugify

class Product(models.Model):
    BUY_CHOICES = (
        ("external", "Buy on startup site"),
        ("internal", "Buy here"),
    )

    startup       = models.ForeignKey(Startup, on_delete=models.CASCADE, related_name="products")
    name          = models.CharField(max_length=255)
    slug          = models.SlugField(max_length=255, unique=True, blank=True)
    tag           = models.CharField(max_length=80, blank=True)
    description   = models.TextField(blank=True)
    image         = models.ImageField(upload_to="products/", blank=True, null=True)
    price         = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    old_price     = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    buy_option    = models.CharField(max_length=8, choices=BUY_CHOICES, default="external")
    external_url  = models.URLField(blank=True, null=True)
    created_at    = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)