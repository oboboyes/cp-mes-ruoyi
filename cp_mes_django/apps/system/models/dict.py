"""
Dictionary models for cp_mes project.
Maps to sys_dict_type and sys_dict_data tables.
"""

from django.db import models


class DictType(models.Model):
    """
    Dictionary type model.
    Maps to sys_dict_type table.
    """
    
    id = models.BigAutoField(primary_key=True)
    dict_name = models.CharField(max_length=100, verbose_name='字典名称')
    dict_type = models.CharField(max_length=100, unique=True, verbose_name='字典类型')
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
        db_table = 'sys_dict_type'
        verbose_name = '字典类型'
        verbose_name_plural = '字典类型'
    
    def __str__(self):
        return self.dict_name
    
    @property
    def is_active(self):
        return self.status == '0'


class DictData(models.Model):
    """
    Dictionary data model.
    Maps to sys_dict_data table.
    """
    
    id = models.BigAutoField(primary_key=True)
    dict_sort = models.IntegerField(default=0, verbose_name='字典排序')
    dict_label = models.CharField(max_length=100, verbose_name='字典标签')
    dict_value = models.CharField(max_length=100, verbose_name='字典键值')
    dict_type = models.CharField(max_length=100, verbose_name='字典类型')
    css_class = models.CharField(max_length=100, null=True, blank=True, verbose_name='样式属性')
    list_class = models.CharField(max_length=100, null=True, blank=True, verbose_name='表格回显样式')
    is_default = models.CharField(
        max_length=1, 
        default='N',
        verbose_name='是否默认'
    )  # Y=是, N=否
    status = models.CharField(
        max_length=1, 
        default='0',
        verbose_name='状态'
    )  # 0=正常, 1=停用
    
    # Audit fields
    create_by = models.BigIntegerField(null=True, blank=True, verbose_name='创建者')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_by = models.BigIntegerField(null=True, blank=True, verbose_name='更新者')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    remark = models.CharField(max_length=500, null=True, blank=True, verbose_name='备注')
    
    class Meta:
        db_table = 'sys_dict_data'
        verbose_name = '字典数据'
        verbose_name_plural = '字典数据'
        ordering = ['dict_sort']
    
    def __str__(self):
        return f'{self.dict_label} ({self.dict_value})'
    
    @property
    def is_active(self):
        return self.status == '0'
    
    @classmethod
    def get_dict_list(cls, dict_type):
        """
        Get dictionary data list by type.
        """
        return cls.objects.filter(
            dict_type=dict_type,
            status='0'
        ).order_by('dict_sort')
    
    @classmethod
    def get_dict_label(cls, dict_type, dict_value):
        """
        Get dictionary label by type and value.
        """
        try:
            data = cls.objects.get(dict_type=dict_type, dict_value=dict_value)
            return data.dict_label
        except cls.DoesNotExist:
            return dict_value
    
    @classmethod
    def get_dict_value(cls, dict_type, dict_label):
        """
        Get dictionary value by type and label.
        """
        try:
            data = cls.objects.get(dict_type=dict_type, dict_label=dict_label)
            return data.dict_value
        except cls.DoesNotExist:
            return dict_label
