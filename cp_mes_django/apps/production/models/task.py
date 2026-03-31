"""
Task model for cp_mes project.
Maps to task table.
"""

from django.db import models


class Task(models.Model):
    """
    Task model.
    Maps to task table.
    """
    
    # Status choices
    STATUS_PENDING = '0'
    STATUS_IN_PROGRESS = '1'
    STATUS_COMPLETED = '2'
    
    STATUS_CHOICES = [
        (STATUS_PENDING, '待执行'),
        (STATUS_IN_PROGRESS, '执行中'),
        (STATUS_COMPLETED, '已完成'),
    ]
    
    id = models.BigAutoField(primary_key=True)
    sheet_id = models.BigIntegerField(verbose_name='工单ID')
    sheet_code = models.CharField(max_length=50, null=True, blank=True, verbose_name='工单编码')
    task_code = models.CharField(max_length=50, verbose_name='任务编码')
    
    # Procedure info
    procedure_id = models.BigIntegerField(verbose_name='工序ID')
    procedure_name = models.CharField(max_length=100, verbose_name='工序名称')
    procedure_code = models.CharField(max_length=50, null=True, blank=True, verbose_name='工序编码')
    
    # Quantity
    quantity = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='任务数量')
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
    
    # Status
    status = models.CharField(
        max_length=1, 
        default=STATUS_PENDING,
        choices=STATUS_CHOICES,
        verbose_name='任务状态'
    )
    sort_order = models.IntegerField(default=0, verbose_name='排序')
    
    # Multi-tenant
    tenant_id = models.BigIntegerField(null=True, blank=True, verbose_name='租户ID')
    
    # Audit fields
    create_by = models.BigIntegerField(null=True, blank=True, verbose_name='创建者')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_by = models.BigIntegerField(null=True, blank=True, verbose_name='更新者')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    remark = models.CharField(max_length=500, null=True, blank=True, verbose_name='备注')
    
    class Meta:
        db_table = 'task'
        verbose_name = '生产任务'
        verbose_name_plural = '生产任务'
        ordering = ['sort_order', '-create_time']
    
    def __str__(self):
        return f'{self.task_code} - {self.procedure_name}'
    
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
