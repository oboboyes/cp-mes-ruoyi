"""
Admin configuration for inventory app.
"""

from django.contrib import admin
from apps.inventory.models import Material, Supplier, SheetMaterial


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    """
    Material admin.
    """
    list_display = [
        'id', 'material_code', 'material_name', 'material_type',
        'quantity', 'safety_stock', 'unit_price', 'supplier_name', 'status'
    ]
    list_filter = ['status', 'material_type']
    search_fields = ['material_code', 'material_name']
    ordering = ['-create_time']
    
    def is_low_stock_display(self, obj):
        return obj.is_low_stock
    is_low_stock_display.short_description = '库存不足'
    is_low_stock_display.boolean = True


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    """
    Supplier admin.
    """
    list_display = [
        'id', 'supplier_code', 'supplier_name', 'contact_person',
        'contact_phone', 'email', 'status'
    ]
    list_filter = ['status']
    search_fields = ['supplier_code', 'supplier_name']
    ordering = ['-create_time']


@admin.register(SheetMaterial)
class SheetMaterialAdmin(admin.ModelAdmin):
    """
    SheetMaterial admin.
    """
    list_display = [
        'id', 'sheet_code', 'material_name',
        'plan_quantity', 'actual_quantity', 'unit'
    ]
    list_filter = ['create_time']
    search_fields = ['sheet_code', 'material_name']
    ordering = ['-create_time']
