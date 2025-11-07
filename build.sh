#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --no-input

# Wait for database to be ready (with retries)
echo "Waiting for database to be ready..."
max_retries=30
retry_count=0
until python manage.py migrate --check 2>/dev/null || [ $retry_count -eq $max_retries ]; do
  echo "Database not ready yet, waiting... (attempt $((retry_count+1))/$max_retries)"
  sleep 2
  retry_count=$((retry_count+1))
done

if [ $retry_count -eq $max_retries ]; then
  echo "Database connection failed after $max_retries attempts"
  exit 1
fi

# Run database migrations
python manage.py migrate

# Restore data automatically (without shell access)
python restore_data.py

# Ensure superuser exists/updated for production admin login
python ensure_superuser.py