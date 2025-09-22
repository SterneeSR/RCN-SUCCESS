#!/bin/bash
# Exit immediately if a command exits with a non-zero status.
set -o errexit

# Create migrations (as you requested)
python manage.py makemigrations

# Apply database migrations
python manage.py migrate

# Create the superuser if it doesn't exist
python manage.py createsuperuser

# Start the Gunicorn server which runs your Django app
gunicorn rcnb.wsgi:application --workers 3 --threads 2 --timeout 60 --log-file -