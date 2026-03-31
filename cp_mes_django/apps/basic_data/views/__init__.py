"""
ViewSets for basic_data app.
"""

from rest_framework import viewsets, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from apps.basic_data.models import Client, Product, Procedure, ProcessRoute, Defect
from apps.basic_data.serializers import (
    ClientSerializer, ProductSerializer, ProcedureSerializer,
    ProcessRouteSerializer, DefectSerializer
)
from apps.core.permissions import IsAuthenticated


class ClientViewSet(viewsets.ModelViewSet):
    """
    Client API ViewSet.
    """
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['client_code', 'client_name', 'status']
    
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
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({'code': 200, 'msg': '新增成功', 'data': serializer.data})
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({'code': 200, 'msg': '修改成功', 'data': serializer.data})
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'code': 200, 'msg': '删除成功', 'data': None})


class ProductViewSet(viewsets.ModelViewSet):
    """
    Product API ViewSet.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['product_code', 'product_name', 'status']
    
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


class ProcedureViewSet(viewsets.ModelViewSet):
    """
    Procedure API ViewSet.
    """
    queryset = Procedure.objects.all()
    serializer_class = ProcedureSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['procedure_code', 'procedure_name', 'status']


class ProcessRouteViewSet(viewsets.ModelViewSet):
    """
    ProcessRoute API ViewSet.
    """
    queryset = ProcessRoute.objects.all()
    serializer_class = ProcessRouteSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['route_code', 'route_name', 'status']


class DefectViewSet(viewsets.ModelViewSet):
    """
    Defect API ViewSet.
    """
    queryset = Defect.objects.all()
    serializer_class = DefectSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['defect_code', 'defect_name', 'status']
