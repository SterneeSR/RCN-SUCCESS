#!/usr/bin/env bash
# Exit on error
set -o errexit

# Collect static files into the STATIC_ROOT directory.
python manage.py collectstatic --no-input --clear

# Create database migrations based on model changes.
# This command does NOT need a database connection.
python manage.py makemigrations --no-input