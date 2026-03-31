"""
Procedure model for cp_mes project.
Maps to procedure_info table.
"""

from django.db import models


class Procedure(models.Model):
    """
    Procedure model.
    Maps to procedure_info table.
    """
    
    id = models.BigAutoField(primary_key=True)
    procedure_code = models.CharField(max_length=50, unique=True, verbose_name='工序编码')
    procedure_name = models.CharField(max_length=100, verbose_name='工序名称')
    procedure_type = models.CharField(max_length=50, null=True, blank=True, verbose_name='工序类型')
    standard_time = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        null=True, 
        blank=True,
        verbose_name='标准工时(分钟)'
    )
    status = models.CharField(
        max_length=1, 
        default='0',
        verbose_name='状态'
    )  # 0=正常, 1=停用
    
    # Multi-tenant
    tenant_id = models.BigIntegerField(null=True, blank=True, verbose_name='租户ID')
    
    # Audit fields
    create_by = models.BigIntegerField(null=True, blank=True, verbose_name='创建者')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_by = models.BigIntegerField(null=True, blank=True, verbose_name='更新者')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    remark = models.CharField(max_length=500, null=True, blank=True, verbose_name='备注')
    
    class Meta:
        db_table = 'procedure_info'
        verbose_name = '工序'
        verbose_name_plural = '工序'
        ordering = ['-create_time']
    
    def __str__(self):
        return self.procedure_name
    
    @property
    def is_active(self):
        return self.status == '0'
