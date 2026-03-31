"""
Supplier model for cp_mes project.
Maps to purveyor_info table.
"""

from django.db import models


class Supplier(models.Model):
    """
    Supplier model.
    Maps to purveyor_info table.
    """
    
    id = models.BigAutoField(primary_key=True)
    supplier_code = models.CharField(max_length=50, unique=True, verbose_name='供应商编码')
    supplier_name = models.CharField(max_length=100, verbose_name='供应商名称')
    contact_person = models.CharField(max_length=50, null=True, blank=True, verbose_name='联系人')
    contact_phone = models.CharField(max_length=20, null=True, blank=True, verbose_name='联系电话')
    email = models.CharField(max_length=50, null=True, blank=True, verbose_name='邮箱')
    address = models.CharField(max_length=200, null=True, blank=True, verbose_name='地址')
    bank_name = models.CharField(max_length=100, null=True, blank=True, verbose_name='开户银行')
    bank_account = models.CharField(max_length=50, null=True, blank=True, verbose_name='银行账号')
    
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
        db_table = 'purveyor_info'
        verbose_name = '供应商'
        verbose_name_plural = '供应商'
        ordering = ['-create_time']
    
    def __str__(self):
        return self.supplier_name
    
    @property
    def is_active(self):
        return self.status == '0'
