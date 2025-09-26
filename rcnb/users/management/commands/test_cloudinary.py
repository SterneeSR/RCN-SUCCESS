from django.core.management.base import BaseCommand
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

class Command(BaseCommand):
    help = "Test Cloudinary upload"

    def handle(self, *args, **kwargs):
        file_name = default_storage.save("railway_test.txt", ContentFile("Hello Cloudinary!"))
        self.stdout.write(f"Uploaded file URL: {default_storage.url(file_name)}")
