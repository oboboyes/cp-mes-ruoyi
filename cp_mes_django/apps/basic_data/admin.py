"""
Admin configuration for basic_data app.
"""

from django.contrib import admin
from apps.basic_data.models import Client, Product, Procedure, ProcessRoute, Defect


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    """
    Client admin.
    """
    list_display = ['id', 'client_code', 'client_name', 'contact_person', 'contact_phone', 'status']
    list_filter = ['status']
    search_fields = ['client_code', 'client_name']
    ordering = ['-create_time']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Product admin.
    """
    list_display = ['id', 'product_code', 'product_name', 'product_type', 'specification', 'unit', 'status']
    list_filter = ['status', 'product_type']
    search_fields = ['product_code', 'product_name']
    ordering = ['-create_time']


@admin.register(Procedure)
class ProcedureAdmin(admin.ModelAdmin):
    """
    Procedure admin.
    """
    list_display = ['id', 'procedure_code', 'procedure_name', 'procedure_type', 'standard_time', 'status']
    list_filter = ['status', 'procedure_type']
    search_fields = ['procedure_code', 'procedure_name']
    ordering = ['-create_time']


@admin.register(ProcessRoute)
class ProcessRouteAdmin(admin.ModelAdmin):
    """
    ProcessRoute admin.
    """
    list_display = ['id', 'route_code', 'route_name', 'product_name', 'status']
    list_filter = ['status']
    search_fields = ['route_code', 'route_name']
    ordering = ['-create_time']


@admin.register(Defect)
class DefectAdmin(admin.ModelAdmin):
    """
    Defect admin.
    """
    list_display = ['id', 'defect_code', 'defect_name', 'defect_type', 'status']
    list_filter = ['status', 'defect_type']
    search_fields = ['defect_code', 'defect_name']
    ordering = ['-create_time']
