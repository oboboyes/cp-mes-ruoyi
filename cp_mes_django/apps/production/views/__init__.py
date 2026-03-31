"""
ViewSets for production app.
"""

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone

from apps.production.models import Sheet, Task, JobBooking
from apps.production.serializers import (
    SheetSerializer, SheetCreateSerializer,
    TaskSerializer, JobBookingSerializer, JobBookingCreateSerializer
)
from apps.core.permissions import IsAuthenticated


class SheetViewSet(viewsets.ModelViewSet):
    """
    Sheet (Work Order) API ViewSet.
    """
    queryset = Sheet.objects.all()
    serializer_class = SheetSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['sheet_code', 'status', 'product_id']
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return SheetCreateSerializer
        return SheetSerializer
    
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
    
    @action(methods=['put'], detail=True)
    def start(self, request, pk=None):
        """Start production."""
        sheet = self.get_object()
        sheet.start_production()
        return Response({'code': 200, 'msg': '生产已开始', 'data': None})
    
    @action(methods=['put'], detail=True)
    def complete(self, request, pk=None):
        """Complete production."""
        sheet = self.get_object()
        sheet.complete_production()
        return Response({'code': 200, 'msg': '生产已完成', 'data': None})
    
    @action(methods=['put'], detail=True)
    def cancel(self, request, pk=None):
        """Cancel work order."""
        sheet = self.get_object()
        sheet.cancel()
        return Response({'code': 200, 'msg': '工单已取消', 'data': None})


class TaskViewSet(viewsets.ModelViewSet):
    """
    Task API ViewSet.
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['sheet_id', 'status', 'procedure_id']
    
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


class JobBookingViewSet(viewsets.ModelViewSet):
    """
    JobBooking API ViewSet.
    """
    queryset = JobBooking.objects.all()
    serializer_class = JobBookingSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['sheet_id', 'task_id', 'procedure_id', 'operator_id']
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return JobBookingCreateSerializer
        return JobBookingSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Set booking time if not provided
        if not serializer.validated_data.get('booking_time'):
            serializer.validated_data['booking_time'] = timezone.now()
        
        self.perform_create(serializer)
        
        # Update task completed quantity
        job_booking = serializer.instance
        try:
            task = Task.objects.get(id=job_booking.task_id)
            task.completed_quantity += job_booking.quantity
            task.defect_quantity += job_booking.defect_quantity
            if task.completed_quantity >= task.quantity:
                task.status = Task.STATUS_COMPLETED
            elif task.completed_quantity > 0:
                task.status = Task.STATUS_IN_PROGRESS
            task.save()
            
            # Update sheet completed quantity
            sheet = Sheet.objects.get(id=job_booking.sheet_id)
            sheet.completed_quantity += job_booking.quantity
            sheet.defect_quantity += job_booking.defect_quantity
            if sheet.completed_quantity >= sheet.quantity:
                sheet.status = Sheet.STATUS_COMPLETED
            elif sheet.completed_quantity > 0:
                sheet.status = Sheet.STATUS_IN_PROGRESS
            sheet.save()
        except (Task.DoesNotExist, Sheet.DoesNotExist):
            pass
        
        return Response({'code': 200, 'msg': '报工成功', 'data': serializer.data})
