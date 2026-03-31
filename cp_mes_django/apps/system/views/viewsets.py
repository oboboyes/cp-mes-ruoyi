"""
ViewSets for system app.
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import get_user_model

from apps.system.models import (
    User, Role, Menu, Dept, Post, Config,
    DictType, DictData, Notice, OperLog, LoginLog
)
from apps.system.serializers import (
    UserSerializer, UserCreateSerializer, RoleSerializer,
    MenuSerializer, MenuTreeSerializer, DeptSerializer,
    DeptTreeSerializer, PostSerializer, ConfigSerializer,
    DictTypeSerializer, DictDataSerializer, NoticeSerializer,
    OperLogSerializer, LoginLogSerializer
)
from apps.core.permissions import IsAuthenticated, DataScopePermission
from apps.core.decorators import log, check_permission, prevent_repeat_submit

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """
    User API ViewSet.
    """
    queryset = User.objects.filter(del_flag='0')
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, DataScopePermission]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['username', 'status', 'dept_id']
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return UserCreateSerializer
        return UserSerializer
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response({
                'code': 200,
                'msg': '获取成功',
                'data': serializer.data
            })
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'code': 200,
            'msg': '获取成功',
            'data': serializer.data
        })
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({
            'code': 200,
            'msg': '新增成功',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({
            'code': 200,
            'msg': '修改成功',
            'data': serializer.data
        })
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.del_flag = '2'
        instance.save()
        return Response({
            'code': 200,
            'msg': '删除成功',
            'data': None
        }, status=status.HTTP_204_NO_CONTENT)
    
    @action(methods=['put'], detail=True)
    def reset_password(self, request, pk=None):
        """Reset user password."""
        user = self.get_object()
        password = request.data.get('password')
        if not password:
            return Response({'code': 400, 'msg': '密码不能为空', 'data': None})
        user.set_password(password)
        user.save()
        return Response({'code': 200, 'msg': '密码重置成功', 'data': None})
    
    @action(methods=['put'], detail=True)
    def change_status(self, request, pk=None):
        """Change user status."""
        user = self.get_object()
        status_val = request.data.get('status')
        if status_val not in ['0', '1']:
            return Response({'code': 400, 'msg': '状态值无效', 'data': None})
        user.status = status_val
        user.save()
        return Response({'code': 200, 'msg': '状态修改成功', 'data': None})


class RoleViewSet(viewsets.ModelViewSet):
    """
    Role API ViewSet.
    """
    queryset = Role.objects.filter(del_flag='0')
    serializer_class = RoleSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['role_name', 'status']
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response({
                'code': 200,
                'msg': '获取成功',
                'data': serializer.data
            })
        serializer = self.get_serializer(queryset, many=True)
        return Response({'code': 200, 'msg': '获取成功', 'data': serializer.data})
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.del_flag = '2'
        instance.save()
        return Response({'code': 200, 'msg': '删除成功', 'data': None})


class MenuViewSet(viewsets.ModelViewSet):
    """
    Menu API ViewSet.
    """
    queryset = Menu.objects.filter(status='0')
    serializer_class = MenuSerializer
    permission_classes = [IsAuthenticated]
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response({'code': 200, 'msg': '获取成功', 'data': serializer.data})
    
    @action(methods=['get'], detail=False)
    def tree(self, request):
        """Get menu tree."""
        menus = Menu.objects.filter(status='0').order_by('order_num')
        serializer = MenuTreeSerializer(menus, many=True)
        return Response({'code': 200, 'msg': '获取成功', 'data': serializer.data})


class DeptViewSet(viewsets.ModelViewSet):
    """
    Dept API ViewSet.
    """
    queryset = Dept.objects.filter(del_flag='0')
    serializer_class = DeptSerializer
    permission_classes = [IsAuthenticated]
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response({'code': 200, 'msg': '获取成功', 'data': serializer.data})
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        # Check if has children
        if Dept.objects.filter(parent_id=instance.id, del_flag='0').exists():
            return Response({'code': 400, 'msg': '存在子部门，不允许删除', 'data': None})
        instance.del_flag = '2'
        instance.save()
        return Response({'code': 200, 'msg': '删除成功', 'data': None})
    
    @action(methods=['get'], detail=False)
    def tree(self, request):
        """Get dept tree."""
        depts = Dept.objects.filter(del_flag='0').order_by('order_num')
        serializer = DeptTreeSerializer(depts, many=True)
        return Response({'code': 200, 'msg': '获取成功', 'data': serializer.data})


class PostViewSet(viewsets.ModelViewSet):
    """
    Post API ViewSet.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response({
                'code': 200,
                'msg': '获取成功',
                'data': serializer.data
            })
        serializer = self.get_serializer(queryset, many=True)
        return Response({'code': 200, 'msg': '获取成功', 'data': serializer.data})


class ConfigViewSet(viewsets.ModelViewSet):
    """
    Config API ViewSet.
    """
    queryset = Config.objects.all()
    serializer_class = ConfigSerializer
    permission_classes = [IsAuthenticated]
    
    @action(methods=['get'], detail=False)
    def get_key(self, request):
        """Get config by key."""
        key = request.query_params.get('configKey')
        if not key:
            return Response({'code': 400, 'msg': '参数不能为空', 'data': None})
        value = Config.get_value(key)
        return Response({'code': 200, 'msg': '获取成功', 'data': value})


class DictTypeViewSet(viewsets.ModelViewSet):
    """
    DictType API ViewSet.
    """
    queryset = DictType.objects.all()
    serializer_class = DictTypeSerializer
    permission_classes = [IsAuthenticated]


class DictDataViewSet(viewsets.ModelViewSet):
    """
    DictData API ViewSet.
    """
    queryset = DictData.objects.all()
    serializer_class = DictDataSerializer
    permission_classes = [IsAuthenticated]
    
    @action(methods=['get'], detail=False)
    def get_by_type(self, request):
        """Get dict data by type."""
        dict_type = request.query_params.get('dictType')
        if not dict_type:
            return Response({'code': 400, 'msg': '参数不能为空', 'data': None})
        data = DictData.get_dict_list(dict_type)
        serializer = self.get_serializer(data, many=True)
        return Response({'code': 200, 'msg': '获取成功', 'data': serializer.data})


class NoticeViewSet(viewsets.ModelViewSet):
    """
    Notice API ViewSet.
    """
    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer
    permission_classes = [IsAuthenticated]


class OperLogViewSet(viewsets.ReadOnlyModelViewSet):
    """
    OperLog API ViewSet (read only).
    """
    queryset = OperLog.objects.all()
    serializer_class = OperLogSerializer
    permission_classes = [IsAuthenticated]
    
    @action(methods=['delete'], detail=False)
    def clean(self, request):
        """Clean all logs."""
        OperLog.objects.all().delete()
        return Response({'code': 200, 'msg': '清空成功', 'data': None})


class LoginLogViewSet(viewsets.ReadOnlyModelViewSet):
    """
    LoginLog API ViewSet (read only).
    """
    queryset = LoginLog.objects.all()
    serializer_class = LoginLogSerializer
    permission_classes = [IsAuthenticated]
    
    @action(methods=['delete'], detail=False)
    def clean(self, request):
        """Clean all logs."""
        LoginLog.objects.all().delete()
        return Response({'code': 200, 'msg': '清空成功', 'data': None})
