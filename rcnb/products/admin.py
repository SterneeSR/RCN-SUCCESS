from django.contrib import admin
from .models import Product


# Register your models here.



@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "startup", "price", "buy_option", "created_at")
    list_filter = ("startup", "buy_option", "created_at")
    search_fields = ("name", "startup__name", "tag")
    prepopulated_fields = {"slug": ("name",)}

