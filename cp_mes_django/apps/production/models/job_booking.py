"""
JobBooking model for cp_mes project.
Maps to job_booking table.
"""

from django.db import models


class JobBooking(models.Model):
    """
    JobBooking model.
    Maps to job_booking table.
    """
    
    id = models.BigAutoField(primary_key=True)
    
    # Work order info
    sheet_id = models.BigIntegerField(verbose_name='工单ID')
    sheet_code = models.CharField(max_length=50, null=True, blank=True, verbose_name='工单编码')
    
    # Task info
    task_id = models.BigIntegerField(verbose_name='任务ID')
    task_code = models.CharField(max_length=50, null=True, blank=True, verbose_name='任务编码')
    
    # Procedure info
    procedure_id = models.BigIntegerField(verbose_name='工序ID')
    procedure_name = models.CharField(max_length=100, verbose_name='工序名称')
    procedure_code = models.CharField(max_length=50, null=True, blank=True, verbose_name='工序编码')
    
    # Quantity
    quantity = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='报工数量')
    defect_quantity = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0,
        verbose_name='不良数量'
    )
    
    # Time
    booking_time = models.DateTimeField(verbose_name='报工时间')
    
    # Operator
    operator_id = models.BigIntegerField(verbose_name='操作员ID')
    operator_name = models.CharField(max_length=50, verbose_name='操作员姓名')
    
    # Defect details (JSON)
    defect_details = models.JSONField(
        default=list, 
        null=True, 
        blank=True,
        verbose_name='不良明细'
    )
    # defect_details format: [{"defect_id": 1, "defect_name": "划伤", "quantity": 5}, ...]
    
    # Multi-tenant
    tenant_id = models.BigIntegerField(null=True, blank=True, verbose_name='租户ID')
    
    # Audit fields
    create_by = models.BigIntegerField(null=True, blank=True, verbose_name='创建者')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_by = models.BigIntegerField(null=True, blank=True, verbose_name='更新者')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    remark = models.CharField(max_length=500, null=True, blank=True, verbose_name='备注')
    
    class Meta:
        db_table = 'job_booking'
        verbose_name = '报工记录'
        verbose_name_plural = '报工记录'
        ordering = ['-booking_time']
    
    def __str__(self):
        return f'{self.sheet_code} - {self.procedure_name} - {self.operator_name}'
    
    @property
    def qualified_quantity(self):
        """
        Calculate qualified quantity.
        """
        return self.quantity - self.defect_quantity
    
    @property
    def quality_rate(self):
        """
        Calculate quality rate.
        """
        if self.quantity == 0:
            return 100
        return round((self.qualified_quantity / self.quantity) * 100, 2)
