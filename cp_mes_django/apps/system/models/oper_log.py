"""
Operation log model for cp_mes project.
Maps to sys_oper_log table.
"""

from django.db import models


class OperLog(models.Model):
    """
    Operation log model.
    Maps to sys_oper_log table.
    """
    
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=50, verbose_name='模块标题')
    business_type = models.IntegerField(default=0, verbose_name='业务类型')
    # 0=其它, 1=新增, 2=修改, 3=删除, 4=授权, 5=导出, 6=导入, 7=强退, 8=生成代码, 9=清空数据
    method = models.CharField(max_length=200, verbose_name='方法名称')
    request_method = models.CharField(max_length=10, null=True, blank=True, verbose_name='请求方式')
    operator_type = models.IntegerField(default=0, verbose_name='操作类别')
    # 0=后台用户, 1=手机端用户
    oper_name = models.CharField(max_length=50, null=True, blank=True, verbose_name='操作人员')
    dept_name = models.CharField(max_length=50, null=True, blank=True, verbose_name='部门名称')
    oper_url = models.CharField(max_length=255, null=True, blank=True, verbose_name='请求URL')
    oper_ip = models.CharField(max_length=128, null=True, blank=True, verbose_name='主机地址')
    oper_location = models.CharField(max_length=255, null=True, blank=True, verbose_name='操作地点')
    oper_param = models.TextField(null=True, blank=True, verbose_name='请求参数')
    json_result = models.TextField(null=True, blank=True, verbose_name='返回参数')
    status = models.IntegerField(default=0, verbose_name='操作状态')
    # 0=正常, 1=异常
    error_msg = models.TextField(null=True, blank=True, verbose_name='错误消息')
    oper_time = models.DateTimeField(auto_now_add=True, verbose_name='操作时间')
    cost_time = models.BigIntegerField(default=0, verbose_name='消耗时间(毫秒)')
    
    # Multi-tenant
    tenant_id = models.BigIntegerField(null=True, blank=True, verbose_name='租户ID')
    
    class Meta:
        db_table = 'sys_oper_log'
        verbose_name = '操作日志'
        verbose_name_plural = '操作日志'
        ordering = ['-oper_time']
    
    def __str__(self):
        return f'{self.title} - {self.oper_name}'
    
    @property
    def is_success(self):
        return self.status == 0
    
    @classmethod
    def create_log(cls, **kwargs):
        """
        Create operation log.
        """
        return cls.objects.create(**kwargs)
