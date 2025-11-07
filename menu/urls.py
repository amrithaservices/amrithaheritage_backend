from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DailySpecialViewSet

router = DefaultRouter()
router.register(r'daily-specials', DailySpecialViewSet, basename='dailyspecial')

urlpatterns = [
    path('', include(router.urls)),
]