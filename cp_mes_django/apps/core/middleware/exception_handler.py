"""
Custom middleware for cp_mes project.
"""

import time
import json
from django.http import JsonResponse
from django.conf import settings
from apps.core.exceptions import BusinessException


class ExceptionHandlerMiddleware:
    """
    Middleware to handle exceptions globally.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        response = self.get_response(request)
        return response
    
    def process_exception(self, request, exception):
        """
        Process exceptions and return consistent error responses.
        """
        if isinstance(exception, BusinessException):
            return JsonResponse({
                'code': exception.code,
                'msg': exception.message,
                'data': None
            }, status=exception.code if exception.code < 500 else 500)
        
        # Log unexpected exceptions
        if settings.DEBUG:
            import traceback
            traceback.print_exc()
        
        return None


class RequestLoggingMiddleware:
    """
    Middleware to log request information.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Skip logging for static files and health checks
        if request.path.startswith('/static/') or request.path == '/health':
            return self.get_response(request)
        
        start_time = time.time()
        
        # Log request
        if settings.DEBUG:
            print(f"[REQUEST] {request.method} {request.path}")
        
        response = self.get_response(request)
        
        # Log response
        duration = time.time() - start_time
        if settings.DEBUG:
            print(f"[RESPONSE] {request.method} {request.path} - {response.status_code} - {duration:.3f}s")
        
        # Add timing header
        response['X-Response-Time'] = f'{duration:.3f}s'
        
        return response


class TenantMiddleware:
    """
    Middleware for multi-tenant support.
    Sets tenant context based on user or domain.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Get tenant from user or domain
        tenant_id = None
        
        # Try to get tenant from authenticated user
        if hasattr(request, 'user') and request.user.is_authenticated:
            tenant_id = getattr(request.user, 'tenant_id', None)
        
        # Try to get tenant from domain
        if not tenant_id:
            host = request.get_host().split(':')[0]
            # Look up tenant by domain (implement as needed)
            # tenant_id = get_tenant_by_domain(host)
        
        # Set tenant in request
        request.tenant_id = tenant_id
        
        response = self.get_response(request)
        
        return response
