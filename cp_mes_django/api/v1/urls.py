"""
API v1 URL configuration.
"""

from django.urls import path, include

urlpatterns = [
    path('system/', include('apps.system.urls')),
    path('basic/', include('apps.basic_data.urls')),
    path('production/', include('apps.production.urls')),
    path('inventory/', include('apps.inventory.urls')),
    path('report/', include('apps.report.urls')),
    path('monitor/', include('apps.monitor.urls')),
]
