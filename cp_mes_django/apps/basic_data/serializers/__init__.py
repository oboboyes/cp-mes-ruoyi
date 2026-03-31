"""
Serializers for basic_data app.
"""

from rest_framework import serializers
from apps.basic_data.models import Client, Product, Procedure, ProcessRoute, Defect


class ClientSerializer(serializers.ModelSerializer):
    """
    Client serializer.
    """
    createTime = serializers.DateTimeField(source='create_time', read_only=True)
    updateTime = serializers.DateTimeField(source='update_time', read_only=True)
    
    class Meta:
        model = Client
        fields = [
            'id', 'client_code', 'client_name', 'contact_person',
            'contact_phone', 'address', 'status', 'create_by',
            'createTime', 'update_by', 'updateTime', 'remark', 'tenant_id'
        ]
        read_only_fields = ['id', 'createTime', 'updateTime']


class ProductSerializer(serializers.ModelSerializer):
    """
    Product serializer.
    """
    createTime = serializers.DateTimeField(source='create_time', read_only=True)
    updateTime = serializers.DateTimeField(source='update_time', read_only=True)
    
    class Meta:
        model = Product
        fields = [
            'id', 'product_code', 'product_name', 'product_type',
            'specification', 'unit', 'status', 'create_by',
            'createTime', 'update_by', 'updateTime', 'remark', 'tenant_id'
        ]
        read_only_fields = ['id', 'createTime', 'updateTime']


class ProcedureSerializer(serializers.ModelSerializer):
    """
    Procedure serializer.
    """
    createTime = serializers.DateTimeField(source='create_time', read_only=True)
    updateTime = serializers.DateTimeField(source='update_time', read_only=True)
    
    class Meta:
        model = Procedure
        fields = [
            'id', 'procedure_code', 'procedure_name', 'procedure_type',
            'standard_time', 'status', 'create_by', 'createTime',
            'update_by', 'updateTime', 'remark', 'tenant_id'
        ]
        read_only_fields = ['id', 'createTime', 'updateTime']


class ProcessRouteSerializer(serializers.ModelSerializer):
    """
    ProcessRoute serializer.
    """
    createTime = serializers.DateTimeField(source='create_time', read_only=True)
    updateTime = serializers.DateTimeField(source='update_time', read_only=True)
    
    class Meta:
        model = ProcessRoute
        fields = [
            'id', 'route_code', 'route_name', 'product_id', 'product_name',
            'procedures', 'status', 'create_by', 'createTime',
            'update_by', 'updateTime', 'remark', 'tenant_id'
        ]
        read_only_fields = ['id', 'createTime', 'updateTime']


class DefectSerializer(serializers.ModelSerializer):
    """
    Defect serializer.
    """
    createTime = serializers.DateTimeField(source='create_time', read_only=True)
    updateTime = serializers.DateTimeField(source='update_time', read_only=True)
    
    class Meta:
        model = Defect
        fields = [
            'id', 'defect_code', 'defect_name', 'defect_type',
            'status', 'create_by', 'createTime', 'update_by',
            'updateTime', 'remark', 'tenant_id'
        ]
        read_only_fields = ['id', 'createTime', 'updateTime']
