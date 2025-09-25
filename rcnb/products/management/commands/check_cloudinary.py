import os
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Check Cloudinary setup, env vars, and test upload"

    def handle(self, *args, **options):
        # Step 1: Check if cloudinary is installed
        try:
            import cloudinary
            import cloudinary.uploader
            self.stdout.write(self.style.SUCCESS("Cloudinary is installed ✅"))
        except ImportError:
            self.stdout.write(self.style.ERROR("Cloudinary is NOT installed ❌"))
            return

        # Step 2: Print environment variables
        cloud_name = os.environ.get("CLOUDINARY_CLOUD_NAME")
        api_key = os.environ.get("CLOUDINARY_API_KEY")
        api_secret = os.environ.get("CLOUDINARY_API_SECRET")

        self.stdout.write(f"CLOUDINARY_CLOUD_NAME: {cloud_name}")
        self.stdout.write(f"CLOUDINARY_API_KEY: {'set' if api_key else 'NOT set'}")
        self.stdout.write(f"CLOUDINARY_API_SECRET: {'set' if api_secret else 'NOT set'}")

        if not all([cloud_name, api_key, api_secret]):
            self.stdout.write(self.style.ERROR("One or more Cloudinary env vars are missing ❌"))
            return

        # Step 3: Test a small image upload
        try:
            result = cloudinary.uploader.upload("https://via.placeholder.com/150.png", folder="test_uploads")
            self.stdout.write(self.style.SUCCESS(f"Upload succeeded ✅ URL: {result['secure_url']}"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Upload failed ❌ {e}"))
