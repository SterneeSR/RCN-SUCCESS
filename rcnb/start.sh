#!/bin/bash
set -o errexit

python manage.py migrate
python manage.py create_superuser_with_password
python manage.py test_cloudinary

gunicorn rcnb.wsgi:application --workers 3 --threads 2 --timeout 60 --log-file
