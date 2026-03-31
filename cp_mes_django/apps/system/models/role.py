"""
Role model for cp_mes project.
Maps to sys_role table.
"""

from django.db import models


class Role(models.Model):
    """
    Role model.
    Maps to sys_role table.
    """
    
    id = models.BigAutoField(primary_key=True)
    role_name = models.CharField(max_length=30, verbose_name='角色名称')
    role_key = models.CharField(max_length=100, verbose_name='角色权限字符串')
    role_sort = models.IntegerField(default=0, verbose_name='显示顺序')
    data_scope = models.CharField(
        max_length=1, 
        default='1',
        verbose_name='数据范围'
    )  # 1=全部, 2=自定义, 3=本部门, 4=本部门及以下, 5=仅本人
    menu_check_strictly = models.BooleanField(default=True, verbose_name='菜单树选择项是否关联显示')
    dept_check_strictly = models.BooleanField(default=True, verbose_name='部门树选择项是否关联显示')
    status = models.CharField(
        max_length=1, 
        default='0',
        verbose_name='角色状态'
    )  # 0=正常, 1=停用
    del_flag = models.CharField(
        max_length=1, 
        default='0',
        verbose_name='删除标志'
    )  # 0=存在, 2=删除
    
    # Multi-tenant
    tenant_id = models.BigIntegerField(null=True, blank=True, verbose_name='租户ID')
    
    # Audit fields
    create_by = models.BigIntegerField(null=True, blank=True, verbose_name='创建者')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_by = models.BigIntegerField(null=True, blank=True, verbose_name='更新者')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    remark = models.CharField(max_length=500, null=True, blank=True, verbose_name='备注')
    
    class Meta:
        db_table = 'sys_role'
        verbose_name = '角色'
        verbose_name_plural = '角色'
        ordering = ['role_sort']
    
    def __str__(self):
        return self.role_name
    
    @property
    def is_active(self):
        return self.status == '0' and self.del_flag == '0'
