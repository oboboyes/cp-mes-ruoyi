"""
URL configuration for report app.
"""

from django.urls import path
from apps.report.views import (
    ProductionStatisticsView,
    DefectAnalysisView,
    ProductOutputView,
    DailyTrendView
)

urlpatterns = [
    path('production/statistics', ProductionStatisticsView.as_view(), name='production-statistics'),
    path('defect/analysis', DefectAnalysisView.as_view(), name='defect-analysis'),
    path('product/output', ProductOutputView.as_view(), name='product-output'),
    path('daily/trend', DailyTrendView.as_view(), name='daily-trend'),
]
