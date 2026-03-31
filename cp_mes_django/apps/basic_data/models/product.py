"""
Product model for cp_mes project.
Maps to product table.
"""

from django.db import models


class Product(models.Model):
    """
    Product model.
    Maps to product table.
    """
    
    id = models.BigAutoField(primary_key=True)
    product_code = models.CharField(max_length=50, unique=True, verbose_name='产品编码')
    product_name = models.CharField(max_length=100, verbose_name='产品名称')
    product_type = models.CharField(max_length=50, null=True, blank=True, verbose_name='产品类型')
    specification = models.CharField(max_length=100, null=True, blank=True, verbose_name='规格型号')
    unit = models.CharField(max_length=20, null=True, blank=True, verbose_name='单位')
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
        db_table = 'product'
        verbose_name = '产品'
        verbose_name_plural = '产品'
        ordering = ['-create_time']
    
    def __str__(self):
        return self.product_name
    
    @property
    def is_active(self):
        return self.status == '0'
