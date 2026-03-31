"""
Custom decorators for cp_mes project.
Equivalent to Java annotations in the original project.
"""

from functools import wraps
from django.core.cache import cache
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
import hashlib
import json
import time


def check_permission(*permissions):
    """
    Decorator to check user permissions.
    Equivalent to @SaCheckPermission in Java.
    
    Usage:
        @check_permission('system:user:list')
        def my_view(request, *args, **kwargs):
            ...
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapped_view(request, *args, **kwargs):
            if not hasattr(request, 'user') or not request.user.is_authenticated:
                return JsonResponse({
                    'code': 401,
                    'msg': '未登录或登录已过期',
                    'data': None
                }, status=401)
            
            user = request.user
            
            # Superuser has all permissions
            if user.is_superuser:
                return view_func(request, *args, **kwargs)
            
            # Check permissions
            user_perms = set(user.get_all_permissions())
            required_perms = set(permissions)
            
            if not required_perms.issubset(user_perms):
                return JsonResponse({
                    'code': 403,
                    'msg': f'没有权限: {", ".join(permissions)}',
                    'data': None
                }, status=403)
            
            return view_func(request, *args, **kwargs)
        return wrapped_view
    return decorator


def check_role(*roles):
    """
    Decorator to check user roles.
    Equivalent to @SaCheckRole in Java.
    
    Usage:
        @check_role('admin', 'manager')
        def my_view(request, *args, **kwargs):
            ...
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapped_view(request, *args, **kwargs):
            if not hasattr(request, 'user') or not request.user.is_authenticated:
                return JsonResponse({
                    'code': 401,
                    'msg': '未登录或登录已过期',
                    'data': None
                }, status=401)
            
            user = request.user
            
            # Superuser has all roles
            if user.is_superuser:
                return view_func(request, *args, **kwargs)
            
            # Check roles
            user_roles = set(getattr(user, 'role_keys', []))
            required_roles = set(roles)
            
            if not required_roles.intersection(user_roles):
                return JsonResponse({
                    'code': 403,
                    'msg': f'需要角色: {", ".join(roles)}',
                    'data': None
                }, status=403)
            
            return view_func(request, *args, **kwargs)
        return wrapped_view
    return decorator


def log(title, business_type=0):
    """
    Decorator for operation logging.
    Equivalent to @Log annotation in Java.
    
    Business types:
        0: 其它
        1: 新增
        2: 修改
        3: 删除
        4: 授权
        5: 导出
        6: 导入
        7: 强退
        8: 生成代码
        9: 清空数据
    
    Usage:
        @log(title='用户管理', business_type=1)
        def create_user(request, *args, **kwargs):
            ...
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapped_view(request, *args, **kwargs):
            start_time = time.time()
            
            # Execute view
            response = view_func(request, *args, **kwargs)
            
            # Calculate cost time
            cost_time = int((time.time() - start_time) * 1000)
            
            # Create log entry asynchronously (in production, use Celery)
            try:
                from apps.system.models import OperLog
                from apps.core.utils.request import get_client_ip, get_user_agent
                
                # Get request data
                request_param = ''
                if request.method in ['POST', 'PUT', 'PATCH']:
                    try:
                        request_param = json.dumps(request.data, ensure_ascii=False)[:2000]
                    except:
                        pass
                elif request.method == 'GET':
                    request_param = json.dumps(dict(request.GET), ensure_ascii=False)[:2000]
                
                # Get response data
                json_result = ''
                if hasattr(response, 'data'):
                    try:
                        json_result = json.dumps(response.data, ensure_ascii=False)[:2000]
                    except:
                        pass
                
                # Create log
                OperLog.objects.create(
                    title=title,
                    business_type=business_type,
                    method=request.resolver_match.view_name if hasattr(request, 'resolver_match') else '',
                    request_method=request.method,
                    operator_type=0,  # Backend operation
                    oper_name=request.user.username if hasattr(request, 'user') and request.user.is_authenticated else None,
                    oper_url=request.path,
                    oper_ip=get_client_ip(request),
                    oper_location='',  # Can be filled with IP location lookup
                    oper_param=request_param,
                    json_result=json_result,
                    status=0 if hasattr(response, 'status_code') and response.status_code < 400 else 1,
                    error_msg='',
                    cost_time=cost_time,
                )
            except Exception as e:
                # Don't fail the request if logging fails
                pass
            
            return response
        return wrapped_view
    return decorator


def rate_limit(key_prefix, rate='10/minute'):
    """
    Rate limiting decorator.
    Equivalent to @RateLimiter in Java.
    
    Usage:
        @rate_limit('api:user', rate='100/hour')
        def my_view(request, *args, **kwargs):
            ...
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapped_view(request, *args, **kwargs):
            # Parse rate
            count, period = rate.split('/')
            period_seconds = {
                'second': 1,
                'minute': 60,
                'hour': 3600,
                'day': 86400
            }.get(period, 60)
            
            # Build cache key
            identifier = ''
            if hasattr(request, 'user') and request.user.is_authenticated:
                identifier = str(request.user.id)
            else:
                from apps.core.utils.request import get_client_ip
                identifier = get_client_ip(request)
            
            cache_key = f"rate_limit:{key_prefix}:{identifier}"
            
            # Check rate
            current = cache.get(cache_key, 0)
            if current >= int(count):
                return JsonResponse({
                    'code': 429,
                    'msg': '请求过于频繁，请稍后再试',
                    'data': None
                }, status=429)
            
            # Increment counter
            cache.set(cache_key, current + 1, period_seconds)
            
            return view_func(request, *args, **kwargs)
        return wrapped_view
    return decorator


def prevent_repeat_submit(interval=5):
    """
    Prevent repeat submission decorator.
    Equivalent to @RepeatSubmit in Java.
    
    Usage:
        @prevent_repeat_submit(interval=3)
        def create_order(request, *args, **kwargs):
            ...
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapped_view(request, *args, **kwargs):
            if request.method in ['POST', 'PUT', 'DELETE']:
                # Build cache key from request data
                try:
                    data = json.dumps(getattr(request, 'data', {}), sort_keys=True)
                except:
                    data = str(getattr(request, 'data', {}))
                
                data_hash = hashlib.md5(data.encode()).hexdigest()
                
                user_id = ''
                if hasattr(request, 'user') and request.user.is_authenticated:
                    user_id = str(request.user.id)
                else:
                    from apps.core.utils.request import get_client_ip
                    user_id = get_client_ip(request)
                
                cache_key = f"repeat_submit:{user_id}:{request.path}:{data_hash}"
                
                if cache.get(cache_key):
                    return JsonResponse({
                        'code': 400,
                        'msg': '请勿重复提交',
                        'data': None
                    }, status=400)
                
                # Set cache
                cache.set(cache_key, True, interval)
            
            return view_func(request, *args, **kwargs)
        return wrapped_view
    return decorator
