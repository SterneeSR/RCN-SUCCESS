# core/urls.py
from django.urls import path
from .views import bulk_upload_view

urlpatterns = [
    path('bulk-upload/', bulk_upload_view, name='bulk_upload'),
]