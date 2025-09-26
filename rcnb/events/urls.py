from django.urls import path
from .views import cloudinary_test

urlpatterns = [
    path("cloudinary-test/", cloudinary_test, name="cloudinary_test"),
]

