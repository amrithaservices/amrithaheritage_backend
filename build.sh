#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --no-input

# Run database migrations
python manage.py migrate

# Restore data automatically (without shell access)
python restore_data.py

# Ensure superuser exists/updated for production admin login
python ensure_superuser.py