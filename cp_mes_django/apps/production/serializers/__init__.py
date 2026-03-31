"""
Serializers for production app.
"""

from rest_framework import serializers
from apps.production.models import Sheet, Task, JobBooking


class SheetSerializer(serializers.ModelSerializer):
    """
    Sheet serializer.
    """
    createTime = serializers.DateTimeField(source='create_time', read_only=True)
    updateTime = serializers.DateTimeField(source='update_time', read_only=True)
    startTime = serializers.DateTimeField(source='start_time', read_only=True)
    endTime = serializers.DateTimeField(source='end_time', read_only=True)
    actualStartTime = serializers.DateTimeField(source='actual_start_time', read_only=True)
    actualEndTime = serializers.DateTimeField(source='actual_end_time', read_only=True)
    progressRate = serializers.FloatField(source='progress_rate', read_only=True)
    remainingQuantity = serializers.DecimalField(
        source='remaining_quantity',
        max_digits=10,
        decimal_places=2,
        read_only=True
    )
    
    class Meta:
        model = Sheet
        fields = [
            'id', 'sheet_code', 'sheet_name', 'product_id', 'product_name',
            'product_code', 'quantity', 'completed_quantity', 'defect_quantity',
            'startTime', 'endTime', 'actualStartTime', 'actualEndTime',
            'status', 'priority', 'process_route_id', 'process_route_name',
            'client_id', 'client_name', 'create_by', 'createTime',
            'update_by', 'updateTime', 'remark', 'tenant_id',
            'progressRate', 'remainingQuantity'
        ]
        read_only_fields = ['id', 'createTime', 'updateTime']


class SheetCreateSerializer(serializers.ModelSerializer):
    """
    Sheet create serializer.
    """
    class Meta:
        model = Sheet
        fields = [
            'id', 'sheet_code', 'sheet_name', 'product_id', 'product_name',
            'product_code', 'quantity', 'start_time', 'end_time',
            'priority', 'process_route_id', 'process_route_name',
            'client_id', 'client_name', 'remark', 'tenant_id'
        ]


class TaskSerializer(serializers.ModelSerializer):
    """
    Task serializer.
    """
    createTime = serializers.DateTimeField(source='create_time', read_only=True)
    updateTime = serializers.DateTimeField(source='update_time', read_only=True)
    progressRate = serializers.FloatField(source='progress_rate', read_only=True)
    remainingQuantity = serializers.DecimalField(
        source='remaining_quantity',
        max_digits=10,
        decimal_places=2,
        read_only=True
    )
    
    class Meta:
        model = Task
        fields = [
            'id', 'sheet_id', 'sheet_code', 'task_code', 'procedure_id',
            'procedure_name', 'procedure_code', 'quantity', 'completed_quantity',
            'defect_quantity', 'status', 'sort_order', 'create_by',
            'createTime', 'update_by', 'updateTime', 'remark', 'tenant_id',
            'progressRate', 'remainingQuantity'
        ]
        read_only_fields = ['id', 'createTime', 'updateTime']


class JobBookingSerializer(serializers.ModelSerializer):
    """
    JobBooking serializer.
    """
    createTime = serializers.DateTimeField(source='create_time', read_only=True)
    updateTime = serializers.DateTimeField(source='update_time', read_only=True)
    bookingTime = serializers.DateTimeField(source='booking_time')
    qualifiedQuantity = serializers.DecimalField(
        source='qualified_quantity',
        max_digits=10,
        decimal_places=2,
        read_only=True
    )
    qualityRate = serializers.FloatField(source='quality_rate', read_only=True)
    
    class Meta:
        model = JobBooking
        fields = [
            'id', 'sheet_id', 'sheet_code', 'task_id', 'task_code',
            'procedure_id', 'procedure_name', 'procedure_code',
            'quantity', 'defect_quantity', 'bookingTime', 'operator_id',
            'operator_name', 'defect_details', 'create_by', 'createTime',
            'update_by', 'updateTime', 'remark', 'tenant_id',
            'qualifiedQuantity', 'qualityRate'
        ]
        read_only_fields = ['id', 'createTime', 'updateTime']


class JobBookingCreateSerializer(serializers.ModelSerializer):
    """
    JobBooking create serializer.
    """
    class Meta:
        model = JobBooking
        fields = [
            'id', 'sheet_id', 'sheet_code', 'task_id', 'task_code',
            'procedure_id', 'procedure_name', 'procedure_code',
            'quantity', 'defect_quantity', 'booking_time', 'operator_id',
            'operator_name', 'defect_details', 'remark', 'tenant_id'
        ]
