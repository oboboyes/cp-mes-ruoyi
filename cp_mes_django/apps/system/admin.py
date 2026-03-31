"""
Admin configuration for system app.
"""

from django.contrib import admin
from apps.system.models import (
    User, Role, Menu, Dept, Post, Config,
    DictType, DictData, Notice, OperLog, LoginLog
)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """
    User admin.
    """
    list_display = ['id', 'username', 'nick_name', 'email', 'phonenumber', 'status', 'create_time']
    list_filter = ['status', 'sex', 'create_time']
    search_fields = ['username', 'nick_name', 'email', 'phonenumber']
    ordering = ['-create_time']
    readonly_fields = ['create_time', 'update_time']
    
    fieldsets = (
        ('基本信息', {
            'fields': ('username', 'nick_name', 'dept_id', 'email', 'phonenumber', 'sex', 'avatar')
        }),
        ('账户信息', {
            'fields': ('password', 'status', 'user_type')
        }),
        ('其他信息', {
            'fields': ('tenant_id', 'remark', 'create_by', 'create_time', 'update_by', 'update_time')
        }),
    )


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    """
    Role admin.
    """
    list_display = ['id', 'role_name', 'role_key', 'role_sort', 'data_scope', 'status', 'create_time']
    list_filter = ['status', 'data_scope', 'create_time']
    search_fields = ['role_name', 'role_key']
    ordering = ['role_sort']


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    """
    Menu admin.
    """
    list_display = ['id', 'menu_name', 'parent_id', 'order_num', 'menu_type', 'status', 'perms']
    list_filter = ['menu_type', 'status', 'visible']
    search_fields = ['menu_name', 'perms']
    ordering = ['order_num']


@admin.register(Dept)
class DeptAdmin(admin.ModelAdmin):
    """
    Dept admin.
    """
    list_display = ['id', 'dept_name', 'parent_id', 'order_num', 'leader', 'phone', 'status']
    list_filter = ['status']
    search_fields = ['dept_name', 'leader', 'phone']
    ordering = ['order_num']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """
    Post admin.
    """
    list_display = ['id', 'post_code', 'post_name', 'post_sort', 'status']
    list_filter = ['status']
    search_fields = ['post_code', 'post_name']
    ordering = ['post_sort']


@admin.register(Config)
class ConfigAdmin(admin.ModelAdmin):
    """
    Config admin.
    """
    list_display = ['id', 'config_name', 'config_key', 'config_value', 'config_type']
    list_filter = ['config_type']
    search_fields = ['config_name', 'config_key']


@admin.register(DictType)
class DictTypeAdmin(admin.ModelAdmin):
    """
    DictType admin.
    """
    list_display = ['id', 'dict_name', 'dict_type', 'status', 'create_time']
    list_filter = ['status']
    search_fields = ['dict_name', 'dict_type']


@admin.register(DictData)
class DictDataAdmin(admin.ModelAdmin):
    """
    DictData admin.
    """
    list_display = ['id', 'dict_sort', 'dict_label', 'dict_value', 'dict_type', 'status']
    list_filter = ['status', 'dict_type']
    search_fields = ['dict_label', 'dict_value']
    ordering = ['dict_sort']


@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    """
    Notice admin.
    """
    list_display = ['id', 'notice_title', 'notice_type', 'status', 'create_time']
    list_filter = ['notice_type', 'status']
    search_fields = ['notice_title']


@admin.register(OperLog)
class OperLogAdmin(admin.ModelAdmin):
    """
    OperLog admin.
    """
    list_display = ['id', 'title', 'business_type', 'oper_name', 'oper_ip', 'status', 'oper_time']
    list_filter = ['business_type', 'status', 'oper_time']
    search_fields = ['title', 'oper_name', 'oper_ip']
    readonly_fields = [f.name for f in OperLog._meta.fields]
    ordering = ['-oper_time']


@admin.register(LoginLog)
class LoginLogAdmin(admin.ModelAdmin):
    """
    LoginLog admin.
    """
    list_display = ['id', 'user_name', 'ipaddr', 'login_location', 'browser', 'status', 'login_time']
    list_filter = ['status', 'login_time']
    search_fields = ['user_name', 'ipaddr']
    readonly_fields = [f.name for f in LoginLog._meta.fields]
    ordering = ['-login_time']
