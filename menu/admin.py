from django.contrib import admin
from .models import DailySpecial

@admin.register(DailySpecial)
class DailySpecialAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['is_active']
    ordering = ['-created_at']