"""
Request utility functions.
"""

import ipaddress
from django.http import HttpRequest


def get_client_ip(request: HttpRequest) -> str:
    """
    Get client IP address from request.
    Handles X-Forwarded-For header for reverse proxy setups.
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        # Get the first IP in the chain
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR', '127.0.0.1')
    
    return ip


def get_user_agent(request: HttpRequest) -> str:
    """
    Get user agent string from request.
    """
    return request.META.get('HTTP_USER_AGENT', '')


def is_valid_ip(ip: str) -> bool:
    """
    Check if a string is a valid IP address.
    """
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False


def is_private_ip(ip: str) -> bool:
    """
    Check if an IP address is private.
    """
    try:
        return ipaddress.ip_address(ip).is_private
    except ValueError:
        return False


def get_request_data(request: HttpRequest) -> dict:
    """
    Get request data from various request methods.
    """
    if request.method == 'GET':
        return dict(request.GET)
    elif request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
        if hasattr(request, 'data'):
            return request.data
        return dict(request.POST)
    return {}


def build_absolute_uri(request: HttpRequest, path: str = '') -> str:
    """
    Build absolute URI for a path.
    """
    return request.build_absolute_uri(path)
