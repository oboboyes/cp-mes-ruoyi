"""
Defect model for cp_mes project.
Maps to defect table.
"""

from django.db import models


class Defect(models.Model):
    """
    Defect model.
    Maps to defect table.
    """
    
    id = models.BigAutoField(primary_key=True)
    defect_code = models.CharField(max_length=50, unique=True, verbose_name='不良项编码')
    defect_name = models.CharField(max_length=100, verbose_name='不良项名称')
    defect_type = models.CharField(max_length=50, null=True, blank=True, verbose_name='不良项类型')
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
        db_table = 'defect'
        verbose_name = '不良项'
        verbose_name_plural = '不良项'
        ordering = ['-create_time']
    
    def __str__(self):
        return self.defect_name
    
    @property
    def is_active(self):
        return self.status == '0'
