#!/usr/bin/env bash
# exit on error
set -o errexit

echo "🔧 Installing dependencies..."
pip install -r requirements.txt

echo "📦 Collecting static files..."
python manage.py collectstatic --no-input

echo "⏳ Waiting for database to be ready..."
max_retries=30
retry_count=0
until python manage.py migrate --check 2>/dev/null || [ $retry_count -eq $max_retries ]; do
  echo "Database not ready yet, waiting... (attempt $((retry_count+1))/$max_retries)"
  sleep 2
  retry_count=$((retry_count+1))
done

if [ $retry_count -eq $max_retries ]; then
  echo "❌ Database connection failed after $max_retries attempts"
  exit 1
fi

echo "🗄️  Running database migrations..."
python manage.py migrate

echo "👤 Creating/updating superuser..."
python ensure_superuser.py

echo "✅ Build completed successfully!"