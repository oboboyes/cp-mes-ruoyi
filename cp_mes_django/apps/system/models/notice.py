"""
Notice model for cp_mes project.
Maps to sys_notice table.
"""

from django.db import models


class Notice(models.Model):
    """
    Notice model.
    Maps to sys_notice table.
    """
    
    id = models.BigAutoField(primary_key=True)
    notice_title = models.CharField(max_length=50, verbose_name='公告标题')
    notice_type = models.CharField(max_length=1, verbose_name='公告类型')  # 1=通知, 2=公告
    notice_content = models.TextField(null=True, blank=True, verbose_name='公告内容')
    status = models.CharField(
        max_length=1, 
        default='0',
        verbose_name='公告状态'
    )  # 0=正常, 1=关闭
    
    # Multi-tenant
    tenant_id = models.BigIntegerField(null=True, blank=True, verbose_name='租户ID')
    
    # Audit fields
    create_by = models.BigIntegerField(null=True, blank=True, verbose_name='创建者')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_by = models.BigIntegerField(null=True, blank=True, verbose_name='更新者')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    remark = models.CharField(max_length=500, null=True, blank=True, verbose_name='备注')
    
    class Meta:
        db_table = 'sys_notice'
        verbose_name = '通知公告'
        verbose_name_plural = '通知公告'
        ordering = ['-create_time']
    
    def __str__(self):
        return self.notice_title
    
    @property
    def is_active(self):
        return self.status == '0'
    
    @property
    def is_notification(self):
        return self.notice_type == '1'
    
    @property
    def is_announcement(self):
        return self.notice_type == '2'
