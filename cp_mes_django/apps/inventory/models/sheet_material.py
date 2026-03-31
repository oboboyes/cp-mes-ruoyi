"""
SheetMaterial model for cp_mes project.
Maps to sheet_material table.
"""

from django.db import models


class SheetMaterial(models.Model):
    """
    SheetMaterial model - Material usage for work order.
    Maps to sheet_material table.
    """
    
    id = models.BigAutoField(primary_key=True)
    
    # Work order
    sheet_id = models.BigIntegerField(verbose_name='工单ID')
    sheet_code = models.CharField(max_length=50, null=True, blank=True, verbose_name='工单编码')
    
    # Material
    material_id = models.BigIntegerField(verbose_name='物料ID')
    material_code = models.CharField(max_length=50, null=True, blank=True, verbose_name='物料编码')
    material_name = models.CharField(max_length=100, verbose_name='物料名称')
    
    # Quantity
    plan_quantity = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name='计划数量'
    )
    actual_quantity = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0,
        verbose_name='实际数量'
    )
    
    # Unit
    unit = models.CharField(max_length=20, null=True, blank=True, verbose_name='单位')
    
    # Multi-tenant
    tenant_id = models.BigIntegerField(null=True, blank=True, verbose_name='租户ID')
    
    # Audit fields
    create_by = models.BigIntegerField(null=True, blank=True, verbose_name='创建者')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_by = models.BigIntegerField(null=True, blank=True, verbose_name='更新者')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    remark = models.CharField(max_length=500, null=True, blank=True, verbose_name='备注')
    
    class Meta:
        db_table = 'sheet_material'
        verbose_name = '工单物料'
        verbose_name_plural = '工单物料'
        ordering = ['-create_time']
    
    def __str__(self):
        return f'{self.sheet_code} - {self.material_name}'
    
    @property
    def usage_rate(self):
        """
        Calculate usage rate.
        """
        if self.plan_quantity == 0:
            return 0
        return round((self.actual_quantity / self.plan_quantity) * 100, 2)
