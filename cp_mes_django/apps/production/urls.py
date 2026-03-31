"""
URL configuration for production app.
"""

from rest_framework.routers import DefaultRouter
from apps.production.views import SheetViewSet, TaskViewSet, JobBookingViewSet

router = DefaultRouter()
router.register(r'sheet', SheetViewSet, basename='sheet')
router.register(r'task', TaskViewSet, basename='task')
router.register(r'jobBooking', JobBookingViewSet, basename='job-booking')

urlpatterns = router.urls
