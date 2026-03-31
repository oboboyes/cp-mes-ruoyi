"""
URL configuration for system app.
"""

from rest_framework.routers import DefaultRouter
from apps.system.views import (
    UserViewSet, RoleViewSet, MenuViewSet, DeptViewSet,
    PostViewSet, ConfigViewSet, DictTypeViewSet, DictDataViewSet,
    NoticeViewSet, OperLogViewSet, LoginLogViewSet
)

router = DefaultRouter()
router.register(r'user', UserViewSet, basename='user')
router.register(r'role', RoleViewSet, basename='role')
router.register(r'menu', MenuViewSet, basename='menu')
router.register(r'dept', DeptViewSet, basename='dept')
router.register(r'post', PostViewSet, basename='post')
router.register(r'config', ConfigViewSet, basename='config')
router.register(r'dict/type', DictTypeViewSet, basename='dict-type')
router.register(r'dict/data', DictDataViewSet, basename='dict-data')
router.register(r'notice', NoticeViewSet, basename='notice')
router.register(r'operlog', OperLogViewSet, basename='operlog')
router.register(r'logininfor', LoginLogViewSet, basename='logininfor')

urlpatterns = router.urls
