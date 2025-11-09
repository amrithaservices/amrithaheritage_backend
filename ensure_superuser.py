#!/usr/bin/env python
"""
Ensures superuser exists with credentials from environment variables.
Safe to run multiple times - will update existing user or create new one.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.contrib.auth import get_user_model

def ensure_superuser():
    """Create or update superuser from environment variables"""
    username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
    password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')
    email = os.environ.get('DJANGO_SUPERUSER_EMAIL', '')

    if not username or not password:
        print("⚠️  DJANGO_SUPERUSER_USERNAME and DJANGO_SUPERUSER_PASSWORD not set")
        print("⚠️  Skipping superuser creation")
        return

    User = get_user_model()

    try:
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                'email': email,
                'is_staff': True,
                'is_superuser': True,
                'is_active': True,
            },
        )
        
        # Always update these fields to ensure correct permissions
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.email = email
        user.set_password(password)
        user.save()
        
        if created:
            print(f"✅ Superuser created: {username}")
        else:
            print(f"✅ Superuser updated: {username}")
            
    except Exception as e:
        print(f"❌ Error ensuring superuser: {e}")
        raise

if __name__ == '__main__':
    ensure_superuser()