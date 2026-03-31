"""
Custom exception handler for Django REST Framework.
"""

from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError as DjangoValidationError
from django.http import Http404


def custom_exception_handler(exc, context):
    """
    Custom exception handler that returns consistent error responses.
    """
    # Call REST framework's default exception handler first
    response = exception_handler(exc, context)
    
    if response is not None:
        # Customize the response format
        custom_response_data = {
            'code': response.status_code,
            'msg': get_error_message(response.data),
            'data': None
        }
        response.data = custom_response_data
    
    return response


def get_error_message(data):
    """
    Extract error message from response data.
    """
    if isinstance(data, str):
        return data
    elif isinstance(data, list):
        return data[0] if data else 'Error'
    elif isinstance(data, dict):
        if 'detail' in data:
            return data['detail']
        elif 'msg' in data:
            return data['msg']
        else:
            # Get first error message
            for key, value in data.items():
                if isinstance(value, list) and value:
                    return f"{key}: {value[0]}"
                elif isinstance(value, str):
                    return f"{key}: {value}"
            return 'Error'
    return 'Unknown error'


class BusinessException(Exception):
    """
    Custom business exception.
    """
    
    def __init__(self, message, code=500):
        self.message = message
        self.code = code
        super().__init__(self.message)


class NotFoundException(BusinessException):
    """Resource not found exception."""
    
    def __init__(self, message='资源不存在'):
        super().__init__(message, 404)


class ForbiddenException(BusinessException):
    """Permission denied exception."""
    
    def __init__(self, message='权限不足'):
        super().__init__(message, 403)


class ValidationException(BusinessException):
    """Validation error exception."""
    
    def __init__(self, message='数据验证失败'):
        super().__init__(message, 400)
