"""
ProcessRoute model for cp_mes project.
Maps to process_route table.
"""

from django.db import models


class ProcessRoute(models.Model):
    """
    ProcessRoute model.
    Maps to process_route table.
    """
    
    id = models.BigAutoField(primary_key=True)
    route_code = models.CharField(max_length=50, unique=True, verbose_name='工艺路线编码')
    route_name = models.CharField(max_length=100, verbose_name='工艺路线名称')
    product_id = models.BigIntegerField(null=True, blank=True, verbose_name='产品ID')
    product_name = models.CharField(max_length=100, null=True, blank=True, verbose_name='产品名称')
    procedures = models.JSONField(default=list, verbose_name='工序列表')
    # procedures format: [{"id": 1, "name": "工序1", "order": 1}, ...]
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
        db_table = 'process_route'
        verbose_name = '工艺路线'
        verbose_name_plural = '工艺路线'
        ordering = ['-create_time']
    
    def __str__(self):
        return self.route_name
    
    @property
    def is_active(self):
        return self.status == '0'
    
    def get_procedures_ordered(self):
        """
        Get procedures in order.
        """
        return sorted(self.procedures, key=lambda x: x.get('order', 0))
