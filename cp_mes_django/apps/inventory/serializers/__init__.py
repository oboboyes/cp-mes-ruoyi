"""
Serializers for inventory app.
"""

from rest_framework import serializers
from apps.inventory.models import Material, Supplier, SheetMaterial


class MaterialSerializer(serializers.ModelSerializer):
    """
    Material serializer.
    """
    createTime = serializers.DateTimeField(source='create_time', read_only=True)
    updateTime = serializers.DateTimeField(source='update_time', read_only=True)
    isLowStock = serializers.BooleanField(source='is_low_stock', read_only=True)
    totalValue = serializers.DecimalField(
        source='total_value',
        max_digits=12,
        decimal_places=2,
        read_only=True
    )
    
    class Meta:
        model = Material
        fields = [
            'id', 'material_code', 'material_name', 'material_type',
            'specification', 'unit', 'quantity', 'safety_stock',
            'unit_price', 'supplier_id', 'supplier_name', 'status',
            'create_by', 'createTime', 'update_by', 'updateTime',
            'remark', 'tenant_id', 'isLowStock', 'totalValue'
        ]
        read_only_fields = ['id', 'createTime', 'updateTime']


class SupplierSerializer(serializers.ModelSerializer):
    """
    Supplier serializer.
    """
    createTime = serializers.DateTimeField(source='create_time', read_only=True)
    updateTime = serializers.DateTimeField(source='update_time', read_only=True)
    
    class Meta:
        model = Supplier
        fields = [
            'id', 'supplier_code', 'supplier_name', 'contact_person',
            'contact_phone', 'email', 'address', 'bank_name',
            'bank_account', 'status', 'create_by', 'createTime',
            'update_by', 'updateTime', 'remark', 'tenant_id'
        ]
        read_only_fields = ['id', 'createTime', 'updateTime']


class SheetMaterialSerializer(serializers.ModelSerializer):
    """
    SheetMaterial serializer.
    """
    createTime = serializers.DateTimeField(source='create_time', read_only=True)
    updateTime = serializers.DateTimeField(source='update_time', read_only=True)
    usageRate = serializers.FloatField(source='usage_rate', read_only=True)
    
    class Meta:
        model = SheetMaterial
        fields = [
            'id', 'sheet_id', 'sheet_code', 'material_id', 'material_code',
            'material_name', 'plan_quantity', 'actual_quantity', 'unit',
            'create_by', 'createTime', 'update_by', 'updateTime',
            'remark', 'tenant_id', 'usageRate'
        ]
        read_only_fields = ['id', 'createTime', 'updateTime']
