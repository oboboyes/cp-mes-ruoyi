"""
URL configuration for basic_data app.
"""

from rest_framework.routers import DefaultRouter
from apps.basic_data.views import ClientViewSet, ProductViewSet, ProcedureViewSet, ProcessRouteViewSet, DefectViewSet

router = DefaultRouter()
router.register(r'client', ClientViewSet, basename='client')
router.register(r'product', ProductViewSet, basename='product')
router.register(r'procedure', ProcedureViewSet, basename='procedure')
router.register(r'processRoute', ProcessRouteViewSet, basename='process-route')
router.register(r'defect', DefectViewSet, basename='defect')

urlpatterns = router.urls
