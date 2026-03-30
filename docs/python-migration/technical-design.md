# Technical Design Document

## 1. Architecture Overview

### 1.1 System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         Nginx (Reverse Proxy)                    │
└─────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Django Application                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐              │
│  │   System    │  │   Basic     │  │  Production │              │
│  │   Module    │  │    Data     │  │   Module    │              │
│  └─────────────┘  └─────────────┘  └─────────────┘              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐              │
│  │  Inventory  │  │   Report    │  │   Monitor   │              │
│  │   Module    │  │   Module    │  │   Module    │              │
│  └─────────────┘  └─────────────┘  └─────────────┘              │
└─────────────────────────────────────────────────────────────────┘
                                  │
                    ┌─────────────┼─────────────┐
                    ▼             ▼             ▼
            ┌───────────┐ ┌───────────┐ ┌───────────┐
            │ PostgreSQL│ │   Redis   │ │  Celery   │
            │  (Main)   │ │  (Cache)  │ │ (Tasks)   │
            └───────────┘ └───────────┘ └───────────┘
```

### 1.2 Django Project Structure

```
cp_mes_django/
├── config/                     # Project configuration
│   ├── __init__.py
│   ├── settings/              # Split settings
│   │   ├── __init__.py
│   │   ├── base.py           # Base settings
│   │   ├── development.py    # Dev settings
│   │   ├── production.py     # Prod settings
│   │   └── testing.py        # Test settings
│   ├── urls.py               # Main URL configuration
│   ├── wsgi.py               # WSGI application
│   └── asgi.py               # ASGI application
│
├── apps/                      # Django applications
│   ├── core/                 # Core utilities
│   │   ├── __init__.py
│   │   ├── apps.py
│   │   ├── middleware/       # Custom middleware
│   │   ├── decorators/       # Custom decorators
│   │   ├── permissions/      # Permission classes
│   │   ├── utils/            # Utility functions
│   │   └── exceptions/       # Custom exceptions
│   │
│   ├── system/               # System management
│   │   ├── __init__.py
│   │   ├── apps.py
│   │   ├── models/           # User, Role, Menu, Dept, etc.
│   │   ├── views/            # API views
│   │   ├── serializers/      # DRF serializers
│   │   ├── services/         # Business logic
│   │   └── urls.py
│   │
│   ├── basic_data/           # Basic data management
│   │   ├── models/           # Client, Product, Procedure, etc.
│   │   ├── views/
│   │   ├── serializers/
│   │   └── urls.py
│   │
│   ├── production/           # Production management
│   │   ├── models/           # Sheet, Task, JobBooking
│   │   ├── views/
│   │   ├── serializers/
│   │   └── urls.py
│   │
│   ├── inventory/            # Inventory management
│   │   ├── models/           # Material, Supplier, Stock
│   │   ├── views/
│   │   ├── serializers/
│   │   └── urls.py
│   │
│   ├── report/               # Reports and statistics
│   │   ├── views/
│   │   ├── services/
│   │   └── urls.py
│   │
│   └── monitor/              # System monitoring
│       ├── views/
│       └── urls.py
│
├── tenants/                   # Multi-tenant support
│   ├── __init__.py
│   ├── middleware.py
│   └── models.py
│
├── tasks/                     # Celery tasks
│   ├── __init__.py
│   ├── celery.py
│   ├── scheduled/            # Scheduled tasks
│   └── async/                # Async tasks
│
├── api/                       # API versioning
│   ├── v1/                   # API version 1
│   │   └── urls.py
│   └── v2/                   # API version 2 (future)
│       └── urls.py
│
├── tests/                     # Test suite
│   ├── unit/
│   ├── integration/
│   └── conftest.py
│
├── scripts/                   # Utility scripts
│   ├── migrate_data.py       # Data migration script
│   └── create_superuser.py
│
├── docker/                    # Docker configuration
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── nginx.conf
│
├── requirements/              # Python dependencies
│   ├── base.txt
│   ├── development.txt
│   ├── production.txt
│   └── testing.txt
│
├── manage.py
└── pyproject.toml            # Project metadata
```

---

## 2. Core Components Design

### 2.1 Authentication System

#### JWT Token Structure

```python
# apps/core/authentication/jwt.py

from rest_framework_simplejwt.tokens import RefreshToken

class CustomAccessToken(RefreshToken):
    """
    Custom JWT token with additional claims
    """
    @classmethod
    def for_user(cls, user):
        token = super().for_user(user)
        
        # Add custom claims
        token['user_id'] = user.id
        token['username'] = user.username
        token['dept_id'] = user.dept_id
        token['roles'] = list(user.roles.values_list('role_key', flat=True))
        token['permissions'] = user.get_all_permissions()
        token['tenant_id'] = user.tenant_id
        
        return token
```

#### Authentication Backend

```python
# apps/core/authentication/backend.py

from django.contrib.auth.backends import ModelBackend
from apps.system.models import User

class JWTAuthenticationBackend(ModelBackend):
    """
    Custom authentication backend for JWT
    """
    
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(username=username)
            if user.check_password(password) and user.is_active:
                return user
        except User.DoesNotExist:
            return None
        
        return None
```

### 2.2 Permission System

#### Permission Decorator (替代 @SaCheckPermission)

```python
# apps/core/decorators/permission.py

from functools import wraps
from django.core.exceptions import PermissionDenied

def check_permission(*permissions):
    """
    Decorator to check user permissions
    Equivalent to @SaCheckPermission in Java
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                raise PermissionDenied("Authentication required")
            
            user_perms = request.user.get_all_permissions()
            if not any(perm in user_perms for perm in permissions):
                raise PermissionDenied(f"Permission required: {permissions}")
            
            return view_func(request, *args, **kwargs)
        return wrapped_view
    return decorator


def check_role(*roles):
    """
    Decorator to check user roles
    Equivalent to @SaCheckRole in Java
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                raise PermissionDenied("Authentication required")
            
            user_roles = request.user.roles.values_list('role_key', flat=True)
            if not any(role in user_roles for role in roles):
                raise PermissionDenied(f"Role required: {roles}")
            
            return view_func(request, *args, **kwargs)
        return wrapped_view
    return decorator
```

#### DRF Permission Class

```python
# apps/core/permissions/data_scope.py

from rest_framework import permissions

class DataScopePermission(permissions.BasePermission):
    """
    Row-level data permission
    Equivalent to @DataPermission in Java
    """
    
    def has_permission(self, request, view):
        return request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        user = request.user
        
        # Super user has all permissions
        if user.is_superuser:
            return True
        
        # Check data scope
        data_scope = user.get_data_scope()
        
        if data_scope == 'ALL':
            return True
        elif data_scope == 'DEPT':
            return obj.dept_id == user.dept_id
        elif data_scope == 'DEPT_AND_CHILD':
            return obj.dept_id in user.get_dept_and_children()
        elif data_scope == 'SELF':
            return obj.create_by == user.id
        elif data_scope == 'CUSTOM':
            return obj.dept_id in user.get_custom_dept_scope()
        
        return False
```

### 2.3 Multi-Tenancy

#### Tenant Middleware

```python
# tenants/middleware.py

from django.db import connection
from tenants.models import Tenant

class TenantMiddleware:
    """
    Multi-tenant middleware
    Sets schema based on tenant from JWT token
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Get tenant from request user
        if hasattr(request, 'user') and request.user.is_authenticated:
            tenant_id = getattr(request.user, 'tenant_id', None)
            if tenant_id:
                try:
                    tenant = Tenant.objects.get(id=tenant_id)
                    connection.set_schema(tenant.schema_name)
                except Tenant.DoesNotExist:
                    pass
        
        response = self.get_response(request)
        
        # Reset to public schema
        connection.set_schema_to_public()
        
        return response
```

#### Tenant-Aware Model

```python
# tenants/models.py

from django.db import models
from django_tenants.models import TenantMixin, DomainMixin

class Tenant(TenantMixin):
    """
    Tenant model for multi-tenancy
    """
    name = models.CharField(max_length=100)
    package = models.ForeignKey('TenantPackage', on_delete=models.PROTECT)
    contact_name = models.CharField(max_length=50)
    contact_phone = models.CharField(max_length=20)
    expire_time = models.DateTimeField(null=True)
    is_active = models.BooleanField(default=True)
    
    auto_create_schema = True
    
    class Meta:
        db_table = 'sys_tenant'


class TenantPackage(models.Model):
    """
    Tenant package definition
    """
    name = models.CharField(max_length=100)
    menu_ids = models.JSONField(default=list)  # Available menus
    max_users = models.IntegerField(default=10)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'sys_tenant_package'
```

### 2.4 Operation Logging

#### Log Decorator (替代 @Log 注解)

```python
# apps/core/decorators/log.py

import json
from functools import wraps
from apps.system.models import OperLog
from apps.core.utils.request import get_client_ip, get_user_agent

def log(title, business_type=0):
    """
    Decorator for operation logging
    Equivalent to @Log annotation in Java
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapped_view(request, *args, **kwargs):
            # Execute view
            response = view_func(request, *args, **kwargs)
            
            # Create log entry
            try:
                OperLog.objects.create(
                    title=title,
                    business_type=business_type,
                    method=request.method,
                    request_method=request.method,
                    oper_url=request.path,
                    oper_ip=get_client_ip(request),
                    oper_location=get_location_by_ip(get_client_ip(request)),
                    oper_name=request.user.username if request.user.is_authenticated else None,
                    oper_param=json.dumps(getattr(request, request.method).dict()),
                    status=0 if response.status_code < 400 else 1,
                    error_msg='' if response.status_code < 400 else str(response.data)
                )
            except Exception:
                pass  # Don't fail the request if logging fails
            
            return response
        return wrapped_view
    return decorator
```

### 2.5 Rate Limiting

```python
# apps/core/decorators/rate_limit.py

from functools import wraps
from django.core.cache import cache
from django.core.exceptions import PermissionDenied

def rate_limit(key_prefix, rate='10/minute'):
    """
    Rate limiting decorator
    Equivalent to @RateLimiter in Java
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapped_view(request, *args, **kwargs):
            # Parse rate
            count, period = rate.split('/')
            period_seconds = {'second': 1, 'minute': 60, 'hour': 3600, 'day': 86400}[period]
            
            # Build cache key
            key = f"rate_limit:{key_prefix}:{request.user.id if request.user.is_authenticated else get_client_ip(request)}"
            
            # Check rate
            current = cache.get(key, 0)
            if current >= int(count):
                raise PermissionDenied("Rate limit exceeded")
            
            # Increment
            cache.set(key, current + 1, period_seconds)
            
            return view_func(request, *args, **kwargs)
        return wrapped_view
    return decorator
```

### 2.6 Repeat Submit Prevention

```python
# apps/core/decorators/repeat_submit.py

import hashlib
import json
from functools import wraps
from django.core.cache import cache
from django.core.exceptions import PermissionDenied

def prevent_repeat_submit(interval=5):
    """
    Prevent repeat submission decorator
    Equivalent to @RepeatSubmit in Java
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapped_view(request, *args, **kwargs):
            if request.method in ['POST', 'PUT', 'DELETE']:
                # Build cache key from request data
                data = json.dumps(getattr(request, request.method).dict(), sort_keys=True)
                data_hash = hashlib.md5(data.encode()).hexdigest()
                key = f"repeat_submit:{request.user.id}:{request.path}:{data_hash}"
                
                if cache.get(key):
                    raise PermissionDenied("Please do not repeat submission")
                
                cache.set(key, True, interval)
            
            return view_func(request, *args, **kwargs)
        return wrapped_view
    return decorator
```

---

## 3. Model Design

### 3.1 User Model

```python
# apps/system/models/user.py

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, password, **extra_fields)


class User(AbstractBaseUser):
    """
    User model
    Maps to sys_user table
    """
    id = models.BigAutoField(primary_key=True)
    username = models.CharField(max_length=50, unique=True)
    nick_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100, null=True)
    phonenumber = models.CharField(max_length=20, null=True)
    sex = models.CharField(max_length=1, choices=[('0', 'Male'), ('1', 'Female')], default='0')
    avatar = models.CharField(max_length=200, null=True)
    password = models.CharField(max_length=200)
    status = models.CharField(max_length=1, default='0')  # 0=Normal, 1=Disabled
    del_flag = models.CharField(max_length=1, default='0')  # 0=Exist, 2=Deleted
    login_ip = models.CharField(max_length=128, null=True)
    login_date = models.DateTimeField(null=True)
    
    # Relationships
    dept = models.ForeignKey('Dept', on_delete=models.SET_NULL, null=True)
    roles = models.ManyToManyField('Role', through='UserRole')
    
    # Multi-tenant
    tenant_id = models.BigIntegerField(null=True)
    
    # Audit fields
    create_by = models.BigIntegerField(null=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_by = models.BigIntegerField(null=True)
    update_time = models.DateTimeField(auto_now=True)
    remark = models.CharField(max_length=500, null=True)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['nick_name']
    
    class Meta:
        db_table = 'sys_user'
```

### 3.2 Role Model

```python
# apps/system/models/role.py

from django.db import models

class Role(models.Model):
    """
    Role model
    Maps to sys_role table
    """
    id = models.BigAutoField(primary_key=True)
    role_name = models.CharField(max_length=50)
    role_key = models.CharField(max_length=100)
    role_sort = models.IntegerField(default=0)
    data_scope = models.CharField(max_length=1, default='1')  # 1=All, 2=Custom, 3=Dept, 4=Dept&Child, 5=Self
    menu_check_strictly = models.BooleanField(default=True)
    dept_check_strictly = models.BooleanField(default=True)
    status = models.CharField(max_length=1, default='0')
    del_flag = models.CharField(max_length=1, default='0')
    
    # Relationships
    menus = models.ManyToManyField('Menu', through='RoleMenu')
    depts = models.ManyToManyField('Dept', through='RoleDept')
    
    # Audit fields
    create_by = models.BigIntegerField(null=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_by = models.BigIntegerField(null=True)
    update_time = models.DateTimeField(auto_now=True)
    remark = models.CharField(max_length=500, null=True)
    
    class Meta:
        db_table = 'sys_role'
```

### 3.3 Production Models

```python
# apps/production/models/sheet.py

from django.db import models

class Sheet(models.Model):
    """
    Work order model
    Maps to sheet table
    """
    id = models.BigAutoField(primary_key=True)
    sheet_code = models.CharField(max_length=50, unique=True)  # Work order code
    sheet_name = models.CharField(max_length=200)  # Work order name
    product_id = models.BigIntegerField()  # Product ID
    product_name = models.CharField(max_length=200)  # Product name
    quantity = models.DecimalField(max_digits=10, decimal_places=2)  # Planned quantity
    completed_quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Completed quantity
    defect_quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Defect quantity
    start_time = models.DateTimeField(null=True)  # Planned start time
    end_time = models.DateTimeField(null=True)  # Planned end time
    actual_start_time = models.DateTimeField(null=True)  # Actual start time
    actual_end_time = models.DateTimeField(null=True)  # Actual end time
    status = models.CharField(max_length=1, default='0')  # 0=Pending, 1=In Progress, 2=Completed, 3=Cancelled
    priority = models.IntegerField(default=0)  # Priority
    
    # Relationships
    process_route = models.ForeignKey('basic_data.ProcessRoute', on_delete=models.SET_NULL, null=True)
    
    # Audit fields
    create_by = models.BigIntegerField(null=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_by = models.BigIntegerField(null=True)
    update_time = models.DateTimeField(auto_now=True)
    remark = models.CharField(max_length=500, null=True)
    
    class Meta:
        db_table = 'sheet'


class Task(models.Model):
    """
    Production task model
    Maps to task table
    """
    id = models.BigAutoField(primary_key=True)
    sheet_id = models.BigIntegerField()  # Work order ID
    task_code = models.CharField(max_length=50)  # Task code
    procedure_id = models.BigIntegerField()  # Procedure ID
    procedure_name = models.CharField(max_length=100)  # Procedure name
    quantity = models.DecimalField(max_digits=10, decimal_places=2)  # Task quantity
    completed_quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=1, default='0')
    sort_order = models.IntegerField(default=0)
    
    class Meta:
        db_table = 'task'


class JobBooking(models.Model):
    """
    Job booking model (报工)
    Maps to job_booking table
    """
    id = models.BigAutoField(primary_key=True)
    sheet_id = models.BigIntegerField()
    task_id = models.BigIntegerField()
    procedure_id = models.BigIntegerField()
    quantity = models.DecimalField(max_digits=10, decimal_places=2)  # Reported quantity
    defect_quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    booking_time = models.DateTimeField()  # Booking time
    operator_id = models.BigIntegerField()  # Operator ID
    operator_name = models.CharField(max_length=50)  # Operator name
    
    class Meta:
        db_table = 'job_booking'
```

---

## 4. API Design

### 4.1 ViewSet Pattern

```python
# apps/system/views/user.py

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from apps.system.models import User
from apps.system.serializers import UserSerializer, UserCreateSerializer
from apps.core.permissions import IsAuthenticated, DataScopePermission
from apps.core.decorators import log, check_permission, prevent_repeat_submit
from apps.core.pagination import PageNumberPagination


class UserViewSet(viewsets.ModelViewSet):
    """
    User API ViewSet
    """
    queryset = User.objects.filter(del_flag='0')
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, DataScopePermission]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['username', 'status', 'dept_id']
    pagination_class = PageNumberPagination
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return UserCreateSerializer
        return UserSerializer
    
    @log(title='User Management', business_type=0)
    @check_permission('system:user:list')
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @log(title='User Management', business_type=1)
    @check_permission('system:user:add')
    @prevent_repeat_submit(interval=3)
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @log(title='User Management', business_type=2)
    @check_permission('system:user:edit')
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @log(title='User Management', business_type=3)
    @check_permission('system:user:remove')
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.del_flag = '2'
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(methods=['put'], detail=True)
    @log(title='Reset Password', business_type=2)
    @check_permission('system:user:resetPwd')
    def reset_password(self, request, pk=None):
        user = self.get_object()
        user.set_password(request.data.get('password'))
        user.save()
        return Response({'message': 'Password reset successfully'})
    
    @action(methods=['put'], detail=True)
    @log(title='Change Status', business_type=2)
    @check_permission('system:user:edit')
    def change_status(self, request, pk=None):
        user = self.get_object()
        user.status = request.data.get('status')
        user.save()
        return Response({'message': 'Status changed successfully'})
```

### 4.2 URL Configuration

```python
# apps/system/urls.py

from rest_framework.routers import DefaultRouter
from apps.system.views import UserViewSet, RoleViewSet, MenuViewSet, DeptViewSet

router = DefaultRouter()
router.register(r'user', UserViewSet, basename='user')
router.register(r'role', RoleViewSet, basename='role')
router.register(r'menu', MenuViewSet, basename='menu')
router.register(r'dept', DeptViewSet, basename='dept')

urlpatterns = router.urls
```

---

## 5. Celery Tasks

### 5.1 Celery Configuration

```python
# tasks/celery.py

from celery import Celery
from django.conf import settings

app = Celery('cp_mes')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


@app.task(bind=True)
def scheduled_task_example(self):
    """
    Example scheduled task
    Converted from XXL-Job
    """
    # Task logic here
    pass
```

### 5.2 Celery Beat Schedule

```python
# config/settings/base.py

CELERY_BEAT_SCHEDULE = {
    'clean-expired-sessions': {
        'task': 'tasks.scheduled.clean_expired_sessions',
        'schedule': 3600.0,  # Every hour
    },
    'generate-daily-report': {
        'task': 'tasks.scheduled.generate_daily_report',
        'schedule': crontab(hour=1, minute=0),  # Daily at 1 AM
    },
}
```

---

## 6. Dependencies

### 6.1 Requirements

```txt
# requirements/base.txt

# Core
Django==5.0
djangorestframework==3.14
psycopg[binary]==3.1.18
gunicorn==21.2.0

# Authentication
djangorestframework-simplejwt==5.3.1
PyJWT==2.8.0

# Database
django-tenants==3.6.1
django-filter==23.5

# Caching
django-redis==5.4.0
redis==5.0.1

# Task Queue
celery==5.3.6
celery-beat==2.5.0

# API
drf-spectacular==0.27.2
django-cors-headers==4.3.1

# Validation
pydantic==2.5.0

# Excel
openpyxl==3.1.2
django-import-export==4.0.0

# Utilities
orjson==3.9.12
python-dotenv==1.0.0

# Monitoring
django-prometheus==2.3.1
```

```txt
# requirements/production.txt

-r base.txt

# Production server
uvicorn[standard]==0.27.0
whitenoise==6.6.0

# Security
django-ratelimit==4.1.0

# Logging
structlog==24.1.0
```

---

## 7. Docker Configuration

### 7.1 Dockerfile

```dockerfile
# docker/Dockerfile

FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements/production.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Run gunicorn
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "4"]
```

### 7.2 Docker Compose

```yaml
# docker/docker-compose.yml

version: '3.8'

services:
  web:
    build:
      context: ..
      dockerfile: docker/Dockerfile
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgres://postgres:password@db:5432/cp_mes
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - db
      - redis
    volumes:
      - static_volume:/app/staticfiles

  db:
    image: postgres:16
    environment:
      - POSTGRES_DB=cp_mes
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data

  celery:
    build:
      context: ..
      dockerfile: docker/Dockerfile
    command: celery -A config worker -l info
    depends_on:
      - db
      - redis

  celery-beat:
    build:
      context: ..
      dockerfile: docker/Dockerfile
    command: celery -A config beat -l info
    depends_on:
      - db
      - redis

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - static_volume:/static
    depends_on:
      - web

volumes:
  postgres_data:
  redis_data:
  static_volume:
```

---

## 8. Testing Strategy

### 8.1 Test Configuration

```python
# tests/conftest.py

import pytest
from django.test import Client
from apps.system.models import User

@pytest.fixture
def api_client():
    return Client()


@pytest.fixture
def authenticated_client(api_client, test_user):
    from rest_framework_simplejwt.tokens import RefreshToken
    
    refresh = RefreshToken.for_user(test_user)
    api_client.defaults['HTTP_AUTHORIZATION'] = f'Bearer {refresh.access_token}'
    return api_client


@pytest.fixture
def test_user(db):
    user = User.objects.create_user(
        username='testuser',
        password='testpassword',
        nick_name='Test User'
    )
    return user
```

### 8.2 Example Test

```python
# tests/unit/test_user.py

import pytest
from django.urls import reverse

class TestUserAPI:
    
    def test_list_users_unauthenticated(self, api_client):
        url = reverse('user-list')
        response = api_client.get(url)
        assert response.status_code == 401
    
    def test_list_users_authenticated(self, authenticated_client):
        url = reverse('user-list')
        response = authenticated_client.get(url)
        assert response.status_code == 200
    
    def test_create_user(self, authenticated_client):
        url = reverse('user-list')
        data = {
            'username': 'newuser',
            'password': 'newpassword',
            'nick_name': 'New User'
        }
        response = authenticated_client.post(url, data, content_type='application/json')
        assert response.status_code == 201
```
