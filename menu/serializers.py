from rest_framework import serializers
from .models import DailySpecial

class DailySpecialSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    
    class Meta:
        model = DailySpecial
        fields = ['id', 'name', 'description', 'price', 'image', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
    
    def get_image(self, obj):
        if obj.image:
            return obj.image.url
        return None

class DailySpecialCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailySpecial
        fields = ['name', 'description', 'price', 'image']