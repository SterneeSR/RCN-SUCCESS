# rcnb/rcnb/wsgi.py

import os
from django.core.wsgi import get_wsgi_application
from django.core.management import call_command

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rcnb.settings')

# --- TEMPORARY CODE TO CHECK CLOUDINARY ---
# This will run the check_cloudinary command every time the app starts.
# The output will be in your Railway deployment logs.
print("--- RUNNING CLOUDINARY CHECK ---")
try:
    call_command('check_cloudinary')
except Exception as e:
    print(f"Error running check_cloudinary: {e}")
print("--- CLOUDINARY CHECK COMPLETE ---")
# --- REMOVE THIS CODE AFTER DEBUGGING ---

application = get_wsgi_application()