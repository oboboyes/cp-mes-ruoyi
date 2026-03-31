"""
Custom permission classes for Django REST Framework.
"""

from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied


class IsAuthenticated(permissions.IsAuthenticated):
    """
    Extended IsAuthenticated permission with custom message.
    """
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            raise PermissionDenied(detail='未登录或登录已过期')
        return True


class IsAdminUser(permissions.IsAdminUser):
    """
    Extended IsAdminUser permission with custom message.
    """
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            raise PermissionDenied(detail='未登录或登录已过期')
        if not request.user.is_staff:
            raise PermissionDenied(detail='需要管理员权限')
        return True


class IsSuperUser(permissions.BasePermission):
    """
    Permission for superuser only.
    """
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            raise PermissionDenied(detail='未登录或登录已过期')
        if not request.user.is_superuser:
            raise PermissionDenied(detail='需要超级管理员权限')
        return True


class DataScopePermission(permissions.BasePermission):
    """
    Row-level data permission.
    Equivalent to @DataPermission in Java.
    
    Data scope types:
        1: 全部数据权限
        2: 自定义数据权限
        3: 本部门数据权限
        4: 本部门及以下数据权限
        5: 仅本人数据权限
    """
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        user = request.user
        
        # Superuser has all permissions
        if user.is_superuser:
            return True
        
        # Get data scope from user's roles
        data_scope = getattr(user, 'data_scope', '5')
        
        if data_scope == '1':
            # All data
            return True
        elif data_scope == '3':
            # Department only
            obj_dept_id = getattr(obj, 'dept_id', None)
            return obj_dept_id == user.dept_id
        elif data_scope == '4':
            # Department and children
            obj_dept_id = getattr(obj, 'dept_id', None)
            dept_ids = getattr(user, 'dept_and_children_ids', [])
            return obj_dept_id in dept_ids
        elif data_scope == '5':
            # Self only
            obj_create_by = getattr(obj, 'create_by', None)
            return obj_create_by == user.id
        elif data_scope == '2':
            # Custom
            custom_dept_ids = getattr(user, 'custom_dept_ids', [])
            obj_dept_id = getattr(obj, 'dept_id', None)
            return obj_dept_id in custom_dept_ids
        
        return False


class TenantPermission(permissions.BasePermission):
    """
    Permission for multi-tenant data isolation.
    """
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        user = request.user
        
        # Superuser can access all tenants
        if user.is_superuser:
            return True
        
        # Check tenant
        user_tenant = getattr(user, 'tenant_id', None)
        obj_tenant = getattr(obj, 'tenant_id', None)
        
        return user_tenant == obj_tenant


class RolePermission(permissions.BasePermission):
    """
    Permission based on user roles.
    """
    
    def __init__(self, allowed_roles=None):
        self.allowed_roles = allowed_roles or []
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            raise PermissionDenied(detail='未登录或登录已过期')
        
        if request.user.is_superuser:
            return True
        
        user_roles = set(getattr(request.user, 'role_keys', []))
        allowed_roles = set(self.allowed_roles)
        
        if not allowed_roles.intersection(user_roles):
            raise PermissionDenied(detail='角色权限不足')
        
        return True
