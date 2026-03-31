"""
Material model for cp_mes project.
Maps to material table.
"""

from django.db import models


class Material(models.Model):
    """
    Material model.
    Maps to material table.
    """
    
    id = models.BigAutoField(primary_key=True)
    material_code = models.CharField(max_length=50, unique=True, verbose_name='物料编码')
    material_name = models.CharField(max_length=100, verbose_name='物料名称')
    material_type = models.CharField(max_length=50, null=True, blank=True, verbose_name='物料类型')
    specification = models.CharField(max_length=100, null=True, blank=True, verbose_name='规格型号')
    unit = models.CharField(max_length=20, null=True, blank=True, verbose_name='单位')
    
    # Quantity
    quantity = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0,
        verbose_name='库存数量'
    )
    safety_stock = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        null=True, 
        blank=True,
        verbose_name='安全库存'
    )
    
    # Price
    unit_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        null=True, 
        blank=True,
        verbose_name='单价'
    )
    
    # Supplier
    supplier_id = models.BigIntegerField(null=True, blank=True, verbose_name='供应商ID')
    supplier_name = models.CharField(max_length=100, null=True, blank=True, verbose_name='供应商名称')
    
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
        db_table = 'material'
        verbose_name = '物料'
        verbose_name_plural = '物料'
        ordering = ['-create_time']
    
    def __str__(self):
        return self.material_name
    
    @property
    def is_active(self):
        return self.status == '0'
    
    @property
    def is_low_stock(self):
        """
        Check if stock is below safety level.
        """
        if self.safety_stock is None:
            return False
        return self.quantity < self.safety_stock
    
    @property
    def total_value(self):
        """
        Calculate total value.
        """
        if self.unit_price is None:
            return 0
        return self.quantity * self.unit_price
    
    def add_stock(self, amount):
        """
        Add stock.
        """
        self.quantity += amount
        self.save(update_fields=['quantity', 'update_time'])
    
    def reduce_stock(self, amount):
        """
        Reduce stock.
        """
        if self.quantity >= amount:
            self.quantity -= amount
            self.save(update_fields=['quantity', 'update_time'])
            return True
        return False
