# rcnb/rcnb/wsgi.py

import os
from django.core.wsgi import get_wsgi_application
from django.core.management import call_command

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rcnb.settings')

# --- TEMPORARY CODE TO TEST COMMANDS ---
print("--- RUNNING TEST COMMAND ---")
try:
    # Call the new, simple test command
    call_command('test_command')
except Exception as e:
    print(f"Error running test_command: {e}")
print("--- TEST COMMAND COMPLETE ---")
# --- REMOVE THIS CODE AFTER DEBUGGING ---

application = get_wsgi_application()