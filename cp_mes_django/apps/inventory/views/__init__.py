"""
ViewSets for inventory app.
"""

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend

from apps.inventory.models import Material, Supplier, SheetMaterial
from apps.inventory.serializers import (
    MaterialSerializer, SupplierSerializer, SheetMaterialSerializer
)
from apps.core.permissions import IsAuthenticated


class MaterialViewSet(viewsets.ModelViewSet):
    """
    Material API ViewSet.
    """
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['material_code', 'material_name', 'status', 'supplier_id']
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response({
                'code': 200,
                'msg': '获取成功',
                'data': serializer.data
            })
        serializer = self.get_serializer(queryset, many=True)
        return Response({'code': 200, 'msg': '获取成功', 'data': serializer.data})
    
    @action(methods=['get'], detail=False)
    def low_stock(self, request):
        """Get materials with low stock."""
        materials = [m for m in Material.objects.all() if m.is_low_stock]
        serializer = self.get_serializer(materials, many=True)
        return Response({'code': 200, 'msg': '获取成功', 'data': serializer.data})
    
    @action(methods=['post'], detail=True)
    def add_stock(self, request, pk=None):
        """Add stock to material."""
        material = self.get_object()
        amount = request.data.get('amount')
        if not amount or amount <= 0:
            return Response({'code': 400, 'msg': '数量必须大于0', 'data': None})
        material.add_stock(amount)
        return Response({'code': 200, 'msg': '入库成功', 'data': None})
    
    @action(methods=['post'], detail=True)
    def reduce_stock(self, request, pk=None):
        """Reduce stock from material."""
        material = self.get_object()
        amount = request.data.get('amount')
        if not amount or amount <= 0:
            return Response({'code': 400, 'msg': '数量必须大于0', 'data': None})
        if material.reduce_stock(amount):
            return Response({'code': 200, 'msg': '出库成功', 'data': None})
        return Response({'code': 400, 'msg': '库存不足', 'data': None})


class SupplierViewSet(viewsets.ModelViewSet):
    """
    Supplier API ViewSet.
    """
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['supplier_code', 'supplier_name', 'status']
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response({
                'code': 200,
                'msg': '获取成功',
                'data': serializer.data
            })
        serializer = self.get_serializer(queryset, many=True)
        return Response({'code': 200, 'msg': '获取成功', 'data': serializer.data})


class SheetMaterialViewSet(viewsets.ModelViewSet):
    """
    SheetMaterial API ViewSet.
    """
    queryset = SheetMaterial.objects.all()
    serializer_class = SheetMaterialSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['sheet_id', 'material_id']
