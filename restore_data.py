#!/usr/bin/env python
"""
Data restoration script for Render deployment without shell access.
This script will automatically restore users and menu data on startup.
"""
import os
import django
import json
from pathlib import Path

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.contrib.auth.models import User
from django.core.management import call_command
from django.db import transaction

def restore_data():
    """Restore data from backup if database is empty"""
    
    # Check if data already exists
    if User.objects.exists():
        print("✅ Users already exist, skipping data restoration")
        return
    
    print("🔄 Starting data restoration...")
    
    # Path to backup file
    backup_file = Path(__file__).parent / 'full_backup.json'
    
    if not backup_file.exists():
        print("❌ Backup file not found, creating default admin user")
        create_default_admin()
        return
    
    try:
        # Load data from backup
        with transaction.atomic():
            call_command('loaddata', str(backup_file))
        print("✅ Data restoration completed successfully")
        
        # Verify restoration
        admin_users = User.objects.filter(is_superuser=True)
        print(f"✅ Restored {admin_users.count()} admin users:")
        for user in admin_users:
            print(f"   - {user.username} ({user.email})")
            
    except Exception as e:
        print(f"❌ Error during data restoration: {e}")
        print("🔄 Creating default admin user as fallback")
        create_default_admin()

def create_default_admin():
    """Create default admin user if restoration fails"""
    try:
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@kohinoor.com',
                password='admin123456'
            )
            print("✅ Default admin user created: admin/admin123456")
        else:
            print("✅ Admin user already exists")
    except Exception as e:
        print(f"❌ Error creating admin user: {e}")

if __name__ == '__main__':
    restore_data()