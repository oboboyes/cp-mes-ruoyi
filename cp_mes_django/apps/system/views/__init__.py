"""
Views package for system app.
"""

from .auth import LoginView, LogoutView, RefreshView, GetInfoView
from .viewsets import (
    UserViewSet, RoleViewSet, MenuViewSet, DeptViewSet,
    PostViewSet, ConfigViewSet, DictTypeViewSet, DictDataViewSet,
    NoticeViewSet, OperLogViewSet, LoginLogViewSet
)

__all__ = [
    'LoginView',
    'LogoutView',
    'RefreshView',
    'GetInfoView',
    'UserViewSet',
    'RoleViewSet',
    'MenuViewSet',
    'DeptViewSet',
    'PostViewSet',
    'ConfigViewSet',
    'DictTypeViewSet',
    'DictDataViewSet',
    'NoticeViewSet',
    'OperLogViewSet',
    'LoginLogViewSet',
]
