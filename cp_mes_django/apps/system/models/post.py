"""
Post model for cp_mes project.
Maps to sys_post table.
"""

from django.db import models


class Post(models.Model):
    """
    Post model.
    Maps to sys_post table.
    """
    
    id = models.BigAutoField(primary_key=True)
    post_code = models.CharField(max_length=64, verbose_name='岗位编码')
    post_name = models.CharField(max_length=50, verbose_name='岗位名称')
    post_sort = models.IntegerField(default=0, verbose_name='显示顺序')
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
        db_table = 'sys_post'
        verbose_name = '岗位'
        verbose_name_plural = '岗位'
        ordering = ['post_sort']
    
    def __str__(self):
        return self.post_name
    
    @property
    def is_active(self):
        return self.status == '0'
