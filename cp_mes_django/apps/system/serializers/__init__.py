"""
Serializers for system app.
"""

from rest_framework import serializers
from apps.system.models import (
    User, Role, Menu, Dept, Post, Config,
    DictType, DictData, Notice, OperLog, LoginLog
)


class UserSerializer(serializers.ModelSerializer):
    """
    User serializer.
    """
    deptName = serializers.CharField(source='dept.dept_name', read_only=True, allow_null=True)
    createTime = serializers.DateTimeField(source='create_time', read_only=True)
    updateTime = serializers.DateTimeField(source='update_time', read_only=True)
    
    class Meta:
        model = User
        fields = [
            'id', 'dept_id', 'username', 'nick_name', 'user_type',
            'email', 'phonenumber', 'sex', 'avatar', 'status',
            'login_ip', 'login_date', 'create_by', 'createTime',
            'update_by', 'updateTime', 'remark', 'tenant_id', 'deptName'
        ]
        read_only_fields = ['id', 'createTime', 'updateTime']


class UserCreateSerializer(serializers.ModelSerializer):
    """
    User create serializer.
    """
    password = serializers.CharField(write_only=True, min_length=6, max_length=20)
    
    class Meta:
        model = User
        fields = [
            'id', 'dept_id', 'username', 'nick_name', 'password',
            'email', 'phonenumber', 'sex', 'avatar', 'status',
            'remark', 'tenant_id'
        ]
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
    
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class RoleSerializer(serializers.ModelSerializer):
    """
    Role serializer.
    """
    createTime = serializers.DateTimeField(source='create_time', read_only=True)
    updateTime = serializers.DateTimeField(source='update_time', read_only=True)
    
    class Meta:
        model = Role
        fields = [
            'id', 'role_name', 'role_key', 'role_sort', 'data_scope',
            'menu_check_strictly', 'dept_check_strictly', 'status',
            'create_by', 'createTime', 'update_by', 'updateTime',
            'remark', 'tenant_id'
        ]
        read_only_fields = ['id', 'createTime', 'updateTime']


class MenuSerializer(serializers.ModelSerializer):
    """
    Menu serializer.
    """
    createTime = serializers.DateTimeField(source='create_time', read_only=True)
    updateTime = serializers.DateTimeField(source='update_time', read_only=True)
    
    class Meta:
        model = Menu
        fields = [
            'id', 'menu_name', 'parent_id', 'order_num', 'path',
            'component', 'query', 'route_name', 'is_frame', 'is_cache',
            'menu_type', 'visible', 'status', 'perms', 'icon',
            'create_by', 'createTime', 'update_by', 'updateTime', 'remark'
        ]
        read_only_fields = ['id', 'createTime', 'updateTime']


class MenuTreeSerializer(serializers.ModelSerializer):
    """
    Menu tree serializer.
    """
    children = serializers.SerializerMethodField()
    
    class Meta:
        model = Menu
        fields = [
            'id', 'menu_name', 'parent_id', 'order_num', 'path',
            'component', 'menu_type', 'visible', 'status', 'perms',
            'icon', 'children'
        ]
    
    def get_children(self, obj):
        children = Menu.objects.filter(parent_id=obj.id, status='0')
        if children.exists():
            return MenuTreeSerializer(children, many=True).data
        return []


class DeptSerializer(serializers.ModelSerializer):
    """
    Dept serializer.
    """
    createTime = serializers.DateTimeField(source='create_time', read_only=True)
    updateTime = serializers.DateTimeField(source='update_time', read_only=True)
    
    class Meta:
        model = Dept
        fields = [
            'id', 'parent_id', 'ancestors', 'dept_name', 'order_num',
            'leader', 'phone', 'email', 'status', 'create_by',
            'createTime', 'update_by', 'updateTime', 'remark', 'tenant_id'
        ]
        read_only_fields = ['id', 'createTime', 'updateTime']


class DeptTreeSerializer(serializers.ModelSerializer):
    """
    Dept tree serializer.
    """
    children = serializers.SerializerMethodField()
    
    class Meta:
        model = Dept
        fields = [
            'id', 'parent_id', 'dept_name', 'order_num',
            'leader', 'phone', 'email', 'status', 'children'
        ]
    
    def get_children(self, obj):
        children = Dept.objects.filter(parent_id=obj.id, del_flag='0')
        if children.exists():
            return DeptTreeSerializer(children, many=True).data
        return []


class PostSerializer(serializers.ModelSerializer):
    """
    Post serializer.
    """
    createTime = serializers.DateTimeField(source='create_time', read_only=True)
    updateTime = serializers.DateTimeField(source='update_time', read_only=True)
    
    class Meta:
        model = Post
        fields = [
            'id', 'post_code', 'post_name', 'post_sort', 'status',
            'create_by', 'createTime', 'update_by', 'updateTime',
            'remark', 'tenant_id'
        ]
        read_only_fields = ['id', 'createTime', 'updateTime']


class ConfigSerializer(serializers.ModelSerializer):
    """
    Config serializer.
    """
    createTime = serializers.DateTimeField(source='create_time', read_only=True)
    updateTime = serializers.DateTimeField(source='update_time', read_only=True)
    
    class Meta:
        model = Config
        fields = [
            'id', 'config_name', 'config_key', 'config_value',
            'config_type', 'create_by', 'createTime', 'update_by',
            'updateTime', 'remark', 'tenant_id'
        ]
        read_only_fields = ['id', 'createTime', 'updateTime']


class DictTypeSerializer(serializers.ModelSerializer):
    """
    DictType serializer.
    """
    createTime = serializers.DateTimeField(source='create_time', read_only=True)
    updateTime = serializers.DateTimeField(source='update_time', read_only=True)
    
    class Meta:
        model = DictType
        fields = [
            'id', 'dict_name', 'dict_type', 'status',
            'create_by', 'createTime', 'update_by', 'updateTime',
            'remark', 'tenant_id'
        ]
        read_only_fields = ['id', 'createTime', 'updateTime']


class DictDataSerializer(serializers.ModelSerializer):
    """
    DictData serializer.
    """
    createTime = serializers.DateTimeField(source='create_time', read_only=True)
    updateTime = serializers.DateTimeField(source='update_time', read_only=True)
    
    class Meta:
        model = DictData
        fields = [
            'id', 'dict_sort', 'dict_label', 'dict_value', 'dict_type',
            'css_class', 'list_class', 'is_default', 'status',
            'create_by', 'createTime', 'update_by', 'updateTime', 'remark'
        ]
        read_only_fields = ['id', 'createTime', 'updateTime']


class NoticeSerializer(serializers.ModelSerializer):
    """
    Notice serializer.
    """
    createTime = serializers.DateTimeField(source='create_time', read_only=True)
    updateTime = serializers.DateTimeField(source='update_time', read_only=True)
    
    class Meta:
        model = Notice
        fields = [
            'id', 'notice_title', 'notice_type', 'notice_content',
            'status', 'create_by', 'createTime', 'update_by',
            'updateTime', 'remark', 'tenant_id'
        ]
        read_only_fields = ['id', 'createTime', 'updateTime']


class OperLogSerializer(serializers.ModelSerializer):
    """
    OperLog serializer.
    """
    operTime = serializers.DateTimeField(source='oper_time', read_only=True)
    
    class Meta:
        model = OperLog
        fields = [
            'id', 'title', 'business_type', 'method', 'request_method',
            'operator_type', 'oper_name', 'dept_name', 'oper_url',
            'oper_ip', 'oper_location', 'oper_param', 'json_result',
            'status', 'error_msg', 'operTime', 'cost_time', 'tenant_id'
        ]


class LoginLogSerializer(serializers.ModelSerializer):
    """
    LoginLog serializer.
    """
    loginTime = serializers.DateTimeField(source='login_time', read_only=True)
    
    class Meta:
        model = LoginLog
        fields = [
            'id', 'user_name', 'ipaddr', 'login_location',
            'browser', 'os', 'status', 'msg', 'loginTime', 'tenant_id'
        ]
