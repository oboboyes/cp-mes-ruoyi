"""
URL configuration for inventory app.
"""

from rest_framework.routers import DefaultRouter
from apps.inventory.views import MaterialViewSet, SupplierViewSet, SheetMaterialViewSet

router = DefaultRouter()
router.register(r'material', MaterialViewSet, basename='material')
router.register(r'supplier', SupplierViewSet, basename='supplier')
router.register(r'sheetMaterial', SheetMaterialViewSet, basename='sheet-material')

urlpatterns = router.urls
