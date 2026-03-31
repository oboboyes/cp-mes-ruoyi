"""
Relationship models for cp_mes project.
Maps to relationship tables (sys_user_role, sys_user_post, sys_role_menu, sys_role_dept).
"""

from django.db import models


class UserRole(models.Model):
    """
    User-Role relationship model.
    Maps to sys_user_role table.
    """
    
    id = models.BigAutoField(primary_key=True)
    user_id = models.BigIntegerField(verbose_name='用户ID')
    role_id = models.BigIntegerField(verbose_name='角色ID')
    
    class Meta:
        db_table = 'sys_user_role'
        verbose_name = '用户角色关联'
        verbose_name_plural = '用户角色关联'
        unique_together = ['user_id', 'role_id']
    
    def __str__(self):
        return f'User {self.user_id} - Role {self.role_id}'


class UserPost(models.Model):
    """
    User-Post relationship model.
    Maps to sys_user_post table.
    """
    
    id = models.BigAutoField(primary_key=True)
    user_id = models.BigIntegerField(verbose_name='用户ID')
    post_id = models.BigIntegerField(verbose_name='岗位ID')
    
    class Meta:
        db_table = 'sys_user_post'
        verbose_name = '用户岗位关联'
        verbose_name_plural = '用户岗位关联'
        unique_together = ['user_id', 'post_id']
    
    def __str__(self):
        return f'User {self.user_id} - Post {self.post_id}'


class RoleMenu(models.Model):
    """
    Role-Menu relationship model.
    Maps to sys_role_menu table.
    """
    
    id = models.BigAutoField(primary_key=True)
    role_id = models.BigIntegerField(verbose_name='角色ID')
    menu_id = models.BigIntegerField(verbose_name='菜单ID')
    
    class Meta:
        db_table = 'sys_role_menu'
        verbose_name = '角色菜单关联'
        verbose_name_plural = '角色菜单关联'
        unique_together = ['role_id', 'menu_id']
    
    def __str__(self):
        return f'Role {self.role_id} - Menu {self.menu_id}'


class RoleDept(models.Model):
    """
    Role-Dept relationship model.
    Maps to sys_role_dept table.
    """
    
    id = models.BigAutoField(primary_key=True)
    role_id = models.BigIntegerField(verbose_name='角色ID')
    dept_id = models.BigIntegerField(verbose_name='部门ID')
    
    class Meta:
        db_table = 'sys_role_dept'
        verbose_name = '角色部门关联'
        verbose_name_plural = '角色部门关联'
        unique_together = ['role_id', 'dept_id']
    
    def __str__(self):
        return f'Role {self.role_id} - Dept {self.dept_id}'
