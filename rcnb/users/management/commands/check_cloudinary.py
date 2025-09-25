# rcnb/users/management/commands/check_cloudinary.py

import os
import io
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Checks Cloudinary setup, env vars, and uploads a test file.'

    def handle(self, *args, **options):
        # Step 1: Check if cloudinary is installed
        try:
            import cloudinary
            import cloudinary.uploader
            import cloudinary.api
            self.stdout.write(self.style.SUCCESS('Cloudinary is installed ✅'))
        except ImportError:
            self.stdout.write(self.style.ERROR('Cloudinary is NOT installed ❌'))
            return

        # Step 2: Print environment variables
        cloud_name = os.environ.get('CLOUDINARY_CLOUD_NAME')
        api_key = os.environ.get('CLOUDINARY_API_KEY')
        api_secret = os.environ.get('CLOUDINARY_API_SECRET')

        if not all([cloud_name, api_key, api_secret]):
            self.stdout.write(self.style.ERROR('Missing Cloudinary environment variables ❌'))
            self.stdout.write(f'CLOUDINARY_CLOUD_NAME={cloud_name}')
            self.stdout.write(f'CLOUDINARY_API_KEY={api_key}')
            self.stdout.write(f'CLOUDINARY_API_SECRET={api_secret}')
            return
        else:
            self.stdout.write(self.style.SUCCESS('Cloudinary environment variables found ✅'))

        # Step 3: Try uploading a dummy file
        try:
            dummy_file = io.BytesIO(b'Test Cloudinary upload')
            dummy_file.name = 'test_upload.txt'

            result = cloudinary.uploader.upload(dummy_file, folder='test_check', resource_type='raw')
            self.stdout.write(self.style.SUCCESS(f'Test file uploaded successfully ✅'))
            self.stdout.write(str(result))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Failed to upload test file ❌'))
            self.stdout.write(str(e))
