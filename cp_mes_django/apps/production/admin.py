"""
Admin configuration for production app.
"""

from django.contrib import admin
from apps.production.models import Sheet, Task, JobBooking


@admin.register(Sheet)
class SheetAdmin(admin.ModelAdmin):
    """
    Sheet admin.
    """
    list_display = [
        'id', 'sheet_code', 'sheet_name', 'product_name',
        'quantity', 'completed_quantity', 'status', 'priority'
    ]
    list_filter = ['status', 'priority', 'create_time']
    search_fields = ['sheet_code', 'sheet_name', 'product_name']
    ordering = ['-create_time']
    readonly_fields = ['completed_quantity', 'defect_quantity', 'actual_start_time', 'actual_end_time']


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """
    Task admin.
    """
    list_display = [
        'id', 'task_code', 'sheet_code', 'procedure_name',
        'quantity', 'completed_quantity', 'status', 'sort_order'
    ]
    list_filter = ['status', 'create_time']
    search_fields = ['task_code', 'sheet_code', 'procedure_name']
    ordering = ['sort_order', '-create_time']
    readonly_fields = ['completed_quantity', 'defect_quantity']


@admin.register(JobBooking)
class JobBookingAdmin(admin.ModelAdmin):
    """
    JobBooking admin.
    """
    list_display = [
        'id', 'sheet_code', 'task_code', 'procedure_name',
        'quantity', 'defect_quantity', 'operator_name', 'booking_time'
    ]
    list_filter = ['booking_time']
    search_fields = ['sheet_code', 'task_code', 'operator_name']
    ordering = ['-booking_time']
    readonly_fields = [f.name for f in JobBooking._meta.fields]
