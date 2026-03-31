"""
User model for cp_mes project.
Maps to sys_user table.
"""

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):
    """
    Custom user manager.
    """
    
    def create_user(self, username, password=None, **extra_fields):
        """
        Create a regular user.
        """
        if not username:
            raise ValueError('用户名不能为空')
        
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, password=None, **extra_fields):
        """
        Create a superuser.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('status', '0')
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('超级用户必须设置 is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('超级用户必须设置 is_superuser=True')
        
        return self.create_user(username, password, **extra_fields)


class User(AbstractBaseUser):
    """
    User model.
    Maps to sys_user table.
    """
    
    # Primary key
    id = models.BigAutoField(primary_key=True)
    
    # Department
    dept_id = models.BigIntegerField(null=True, blank=True, verbose_name='部门ID')
    
    # Basic info
    username = models.CharField(
        max_length=30, 
        unique=True, 
        db_column='user_name',
        verbose_name='用户名'
    )
    nick_name = models.CharField(max_length=30, verbose_name='用户昵称')
    user_type = models.CharField(
        max_length=10, 
        default='sys_user',
        verbose_name='用户类型'
    )
    email = models.CharField(
        max_length=50, 
        null=True, 
        blank=True,
        verbose_name='用户邮箱'
    )
    phonenumber = models.CharField(
        max_length=11, 
        null=True, 
        blank=True,
        verbose_name='手机号码'
    )
    sex = models.CharField(
        max_length=1, 
        default='0',
        verbose_name='用户性别'
    )  # 0=男, 1=女, 2=未知
    avatar = models.CharField(
        max_length=100, 
        null=True, 
        blank=True,
        verbose_name='头像地址'
    )
    password = models.CharField(max_length=100, verbose_name='密码')
    
    # Status
    status = models.CharField(
        max_length=1, 
        default='0',
        verbose_name='帐号状态'
    )  # 0=正常, 1=停用
    del_flag = models.CharField(
        max_length=1, 
        default='0',
        verbose_name='删除标志'
    )  # 0=存在, 2=删除
    
    # Login info
    login_ip = models.CharField(
        max_length=128, 
        null=True, 
        blank=True,
        verbose_name='最后登录IP'
    )
    login_date = models.DateTimeField(
        null=True, 
        blank=True,
        verbose_name='最后登录时间'
    )
    
    # Multi-tenant
    tenant_id = models.BigIntegerField(
        null=True, 
        blank=True,
        verbose_name='租户ID'
    )
    
    # Audit fields
    create_by = models.BigIntegerField(null=True, blank=True, verbose_name='创建者')
    create_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name='创建时间'
    )
    update_by = models.BigIntegerField(null=True, blank=True, verbose_name='更新者')
    update_time = models.DateTimeField(
        auto_now=True,
        verbose_name='更新时间'
    )
    remark = models.CharField(
        max_length=500, 
        null=True, 
        blank=True,
        verbose_name='备注'
    )
    
    # Django auth fields
    is_staff = models.BooleanField(default=False, verbose_name='是否员工')
    is_active = models.BooleanField(default=True, verbose_name='是否激活')
    is_superuser = models.BooleanField(default=False, verbose_name='超级用户')
    
    objects = UserManager()
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['nick_name']
    
    class Meta:
        db_table = 'sys_user'
        verbose_name = '用户'
        verbose_name_plural = '用户'
        ordering = ['-create_time']
    
    def __str__(self):
        return self.username
    
    @property
    def is_admin(self):
        return self.is_superuser or self.is_staff
    
    def get_full_name(self):
        return self.nick_name or self.username
    
    def get_short_name(self):
        return self.username
    
    def has_perm(self, perm, obj=None):
        """Always True for superuser, check role permissions otherwise."""
        if self.is_superuser:
            return True
        # Simple permission check - can be enhanced
        return True
    
    def has_perms(self, perm_list, obj=None):
        """Check multiple permissions."""
        return all(self.has_perm(perm, obj) for perm in perm_list)
    
    def has_module_perms(self, app_label):
        """Check module permissions."""
        if self.is_superuser:
            return True
        return True
    
    def get_all_permissions(self):
        """
        Get all permissions for the user.
        """
        if self.is_superuser:
            return set()
        
        perms = set()
        for role in self.roles.all():
            for menu in role.menus.filter(perms__isnull=False).exclude(perms=''):
                perms.add(menu.perms)
        return perms
    
    def get_data_scope(self):
        """
        Get the highest data scope from user's roles.
        """
        if self.is_superuser:
            return '1'  # All data
        
        scopes = list(self.roles.values_list('data_scope', flat=True))
        if not scopes:
            return '5'  # Self only
        
        # Return the most permissive scope
        scope_order = {'1': 1, '2': 2, '3': 3, '4': 4, '5': 5}
        return min(scopes, key=lambda x: scope_order.get(x, 5))
