"""
Config model for cp_mes project.
Maps to sys_config table.
"""

from django.db import models
from django.core.cache import cache


class Config(models.Model):
    """
    System config model.
    Maps to sys_config table.
    """
    
    id = models.BigAutoField(primary_key=True)
    config_name = models.CharField(max_length=100, verbose_name='参数名称')
    config_key = models.CharField(max_length=100, unique=True, verbose_name='参数键名')
    config_value = models.CharField(max_length=500, verbose_name='参数键值')
    config_type = models.CharField(
        max_length=1, 
        default='N',
        verbose_name='系统内置'
    )  # Y=是, N=否
    
    # Multi-tenant
    tenant_id = models.BigIntegerField(null=True, blank=True, verbose_name='租户ID')
    
    # Audit fields
    create_by = models.BigIntegerField(null=True, blank=True, verbose_name='创建者')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_by = models.BigIntegerField(null=True, blank=True, verbose_name='更新者')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    remark = models.CharField(max_length=500, null=True, blank=True, verbose_name='备注')
    
    class Meta:
        db_table = 'sys_config'
        verbose_name = '参数配置'
        verbose_name_plural = '参数配置'
    
    def __str__(self):
        return self.config_name
    
    @property
    def is_builtin(self):
        return self.config_type == 'Y'
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Clear cache when config is saved
        cache.delete(f'config:{self.config_key}')
    
    @classmethod
    def get_value(cls, key, default=None):
        """
        Get config value by key.
        """
        cache_key = f'config:{key}'
        value = cache.get(cache_key)
        
        if value is None:
            try:
                config = cls.objects.get(config_key=key)
                value = config.config_value
                cache.set(cache_key, value, timeout=3600)
            except cls.DoesNotExist:
                return default
        
        return value
    
    @classmethod
    def set_value(cls, key, value):
        """
        Set config value by key.
        """
        config, created = cls.objects.update_or_create(
            config_key=key,
            defaults={'config_value': value}
        )
        return config
