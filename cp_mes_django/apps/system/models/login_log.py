"""
Login log model for cp_mes project.
Maps to sys_logininfor table.
"""

from django.db import models


class LoginLog(models.Model):
    """
    Login log model.
    Maps to sys_logininfor table.
    """
    
    id = models.BigAutoField(primary_key=True)
    user_name = models.CharField(max_length=50, null=True, blank=True, verbose_name='用户账号')
    ipaddr = models.CharField(max_length=128, null=True, blank=True, verbose_name='登录IP地址')
    login_location = models.CharField(max_length=255, null=True, blank=True, verbose_name='登录地点')
    browser = models.CharField(max_length=50, null=True, blank=True, verbose_name='浏览器类型')
    os = models.CharField(max_length=50, null=True, blank=True, verbose_name='操作系统')
    status = models.CharField(
        max_length=1, 
        default='0',
        verbose_name='登录状态'
    )  # 0=成功, 1=失败
    msg = models.CharField(max_length=255, null=True, blank=True, verbose_name='提示消息')
    login_time = models.DateTimeField(auto_now_add=True, verbose_name='访问时间')
    
    # Multi-tenant
    tenant_id = models.BigIntegerField(null=True, blank=True, verbose_name='租户ID')
    
    class Meta:
        db_table = 'sys_logininfor'
        verbose_name = '登录日志'
        verbose_name_plural = '登录日志'
        ordering = ['-login_time']
    
    def __str__(self):
        return f'{self.user_name} - {self.login_time}'
    
    @property
    def is_success(self):
        return self.status == '0'
    
    @classmethod
    def create_log(cls, username, ip, location, browser, os, status, msg, tenant_id=None):
        """
        Create login log.
        """
        return cls.objects.create(
            user_name=username,
            ipaddr=ip,
            login_location=location,
            browser=browser,
            os=os,
            status=status,
            msg=msg,
            tenant_id=tenant_id
        )
