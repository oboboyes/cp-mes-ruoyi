"""
URL configuration for monitor app.
"""

from django.urls import path
from apps.monitor.views import (
    CacheInfoView,
    ServerInfoView,
    DatabaseInfoView,
    OnlineUserView,
    SystemStatsView
)

urlpatterns = [
    path('cache', CacheInfoView.as_view(), name='cache-info'),
    path('server', ServerInfoView.as_view(), name='server-info'),
    path('database', DatabaseInfoView.as_view(), name='database-info'),
    path('online', OnlineUserView.as_view(), name='online-user'),
    path('stats', SystemStatsView.as_view(), name='system-stats'),
]
