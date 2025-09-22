#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -o errexit

# Install Python dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --no-input

# Wait for the database to be ready
# This will try to connect to the database up to 10 times with a 3-second delay.
echo "Waiting for database to be ready..."
for i in {1..10}; do
    if python manage.py dbshell --command "SELECT 1" &> /dev/null; then
        echo "Database is ready."
        break
    fi
    echo "Database not ready, waiting 3 seconds..."
    sleep 3
done

# Apply database migrations
python manage.py migrate

# Create superuser if it doesn't exist
python manage.py create_superuser_with_password