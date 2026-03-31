"""
Sheet (Work Order) model for cp_mes project.
Maps to sheet table.
"""

from django.db import models
from django.utils import timezone


class Sheet(models.Model):
    """
    Sheet (Work Order) model.
    Maps to sheet table.
    """
    
    # Status choices
    STATUS_PENDING = '0'
    STATUS_IN_PROGRESS = '1'
    STATUS_COMPLETED = '2'
    STATUS_CANCELLED = '3'
    
    STATUS_CHOICES = [
        (STATUS_PENDING, '待生产'),
        (STATUS_IN_PROGRESS, '生产中'),
        (STATUS_COMPLETED, '已完成'),
        (STATUS_CANCELLED, '已取消'),
    ]
    
    id = models.BigAutoField(primary_key=True)
    sheet_code = models.CharField(max_length=50, unique=True, verbose_name='工单编码')
    sheet_name = models.CharField(max_length=200, verbose_name='工单名称')
    
    # Product info
    product_id = models.BigIntegerField(verbose_name='产品ID')
    product_name = models.CharField(max_length=200, verbose_name='产品名称')
    product_code = models.CharField(max_length=50, null=True, blank=True, verbose_name='产品编码')
    
    # Quantity
    quantity = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='计划数量')
    completed_quantity = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0,
        verbose_name='完成数量'
    )
    defect_quantity = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0,
        verbose_name='不良数量'
    )
    
    # Time
    start_time = models.DateTimeField(null=True, blank=True, verbose_name='计划开始时间')
    end_time = models.DateTimeField(null=True, blank=True, verbose_name='计划结束时间')
    actual_start_time = models.DateTimeField(null=True, blank=True, verbose_name='实际开始时间')
    actual_end_time = models.DateTimeField(null=True, blank=True, verbose_name='实际结束时间')
    
    # Status and priority
    status = models.CharField(
        max_length=1, 
        default=STATUS_PENDING,
        choices=STATUS_CHOICES,
        verbose_name='工单状态'
    )
    priority = models.IntegerField(default=0, verbose_name='优先级')
    
    # Process route
    process_route_id = models.BigIntegerField(null=True, blank=True, verbose_name='工艺路线ID')
    process_route_name = models.CharField(max_length=100, null=True, blank=True, verbose_name='工艺路线名称')
    
    # Client
    client_id = models.BigIntegerField(null=True, blank=True, verbose_name='客户ID')
    client_name = models.CharField(max_length=100, null=True, blank=True, verbose_name='客户名称')
    
    # Multi-tenant
    tenant_id = models.BigIntegerField(null=True, blank=True, verbose_name='租户ID')
    
    # Audit fields
    create_by = models.BigIntegerField(null=True, blank=True, verbose_name='创建者')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_by = models.BigIntegerField(null=True, blank=True, verbose_name='更新者')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    remark = models.CharField(max_length=500, null=True, blank=True, verbose_name='备注')
    
    class Meta:
        db_table = 'sheet'
        verbose_name = '生产工单'
        verbose_name_plural = '生产工单'
        ordering = ['-create_time']
    
    def __str__(self):
        return f'{self.sheet_code} - {self.sheet_name}'
    
    @property
    def is_pending(self):
        return self.status == self.STATUS_PENDING
    
    @property
    def is_in_progress(self):
        return self.status == self.STATUS_IN_PROGRESS
    
    @property
    def is_completed(self):
        return self.status == self.STATUS_COMPLETED
    
    @property
    def is_cancelled(self):
        return self.status == self.STATUS_CANCELLED
    
    @property
    def progress_rate(self):
        """
        Calculate progress rate.
        """
        if self.quantity == 0:
            return 0
        return round((self.completed_quantity / self.quantity) * 100, 2)
    
    @property
    def remaining_quantity(self):
        """
        Calculate remaining quantity.
        """
        return self.quantity - self.completed_quantity - self.defect_quantity
    
    def start_production(self):
        """
        Start production.
        """
        if self.is_pending:
            self.status = self.STATUS_IN_PROGRESS
            self.actual_start_time = timezone.now()
            self.save(update_fields=['status', 'actual_start_time', 'update_time'])
    
    def complete_production(self):
        """
        Complete production.
        """
        if self.is_in_progress:
            self.status = self.STATUS_COMPLETED
            self.actual_end_time = timezone.now()
            self.save(update_fields=['status', 'actual_end_time', 'update_time'])
    
    def cancel(self):
        """
        Cancel work order.
        """
        if not self.is_completed:
            self.status = self.STATUS_CANCELLED
            self.save(update_fields=['status', 'update_time'])
