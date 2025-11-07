from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from .models import DailySpecial
from .serializers import DailySpecialSerializer, DailySpecialCreateSerializer

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import requests




class DailySpecialViewSet(viewsets.ModelViewSet):
    queryset = DailySpecial.objects.all()
    serializer_class = DailySpecialSerializer
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return DailySpecialCreateSerializer
        return DailySpecialSerializer

    @action(detail=False, methods=['get'])
    def active(self, request):
        """Get only active daily specials"""
        active_specials = self.queryset.filter(is_active=True)
        serializer = self.get_serializer(active_specials, many=True)
        return Response({
            'results': serializer.data,
            'count': active_specials.count()
        })

    @action(detail=True, methods=['post'])
    def toggle_active(self, request, pk=None):
        """Toggle the is_active status of a daily special"""
        special = self.get_object()
        special.is_active = not special.is_active
        special.save()
        serializer = self.get_serializer(special)
        return Response({
            'message': f"Daily special {'activated' if special.is_active else 'deactivated'} successfully",
            'data': serializer.data
        })
