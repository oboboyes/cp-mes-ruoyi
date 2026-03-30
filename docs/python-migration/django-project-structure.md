# Django Project Structure

## 1. Directory Layout

```
cp_mes_django/
│
├── .github/                          # GitHub workflows
│   └── workflows/
│       ├── ci.yml                    # CI pipeline
│       └── deploy.yml                # CD pipeline
│
├── config/                           # Project configuration
│   ├── __init__.py
│   ├── settings/                     # Split settings pattern
│   │   ├── __init__.py
│   │   ├── base.py                   # Common settings
│   │   ├── development.py            # Dev-specific settings
│   │   ├── production.py             # Prod-specific settings
│   │   └── testing.py                # Test-specific settings
│   ├── urls.py                       # Root URL configuration
│   ├── wsgi.py                       # WSGI entry point
│   └── asgi.py                       # ASGI entry point
│
├── apps/                             # Django applications
│   │
│   ├── core/                         # Core utilities (shared)
│   │   ├── __init__.py
│   │   ├── apps.py                   # AppConfig
│   │   │
│   │   ├── authentication/           # Authentication components
│   │   │   ├── __init__.py
│   │   │   ├── jwt.py               # JWT token handling
│   │   │   └── backend.py           # Custom auth backend
│   │   │
│   │   ├── decorators/               # Custom decorators
│   │   │   ├── __init__.py
│   │   │   ├── permission.py        # @check_permission, @check_role
│   │   │   ├── log.py               # @log (operation logging)
│   │   │   ├── rate_limit.py        # @rate_limit
│   │   │   └── repeat_submit.py     # @prevent_repeat_submit
│   │   │
│   │   ├── middleware/               # Custom middleware
│   │   │   ├── __init__.py
│   │   │   ├── request_logging.py   # Request logging
│   │   │   ├── exception_handler.py # Global exception handling
│   │   │   └── tenant.py            # Tenant context
│   │   │
│   │   ├── permissions/              # DRF permission classes
│   │   │   ├── __init__.py
│   │   │   ├── data_scope.py        # Row-level permission
│   │   │   └── tenant.py            # Tenant permission
│   │   │
│   │   ├── utils/                    # Utility functions
│   │   │   ├── __init__.py
│   │   │   ├── request.py           # Request helpers (IP, UA)
│   │   │   ├── datetime.py          # Date/time utilities
│   │   │   ├── encryption.py        # Encryption utilities
│   │   │   ├── excel.py             # Excel utilities
│   │   │   └── tree.py              # Tree structure utilities
│   │   │
│   │   ├── exceptions/               # Custom exceptions
│   │   │   ├── __init__.py
│   │   │   └── business.py          # Business exceptions
│   │   │
│   │   ├── mixins/                   # View mixins
│   │   │   ├── __init__.py
│   │   │   └── audit.py             # Audit field mixin
│   │   │
│   │   └── constants/                # Constants
│   │       ├── __init__.py
│   │       ├── status.py            # Status codes
│   │       └── error_codes.py       # Error codes
│   │
│   ├── system/                       # System management module
│   │   ├── __init__.py
│   │   ├── apps.py
│   │   │
│   │   ├── models/                   # Models
│   │   │   ├── __init__.py
│   │   │   ├── user.py              # User model
│   │   │   ├── role.py              # Role model
│   │   │   ├── menu.py              # Menu model
│   │   │   ├── dept.py              # Department model
│   │   │   ├── post.py              # Post model
│   │   │   ├── dict.py              # Dictionary models
│   │   │   ├── config.py            # Config model
│   │   │   ├── oper_log.py          # Operation log
│   │   │   ├── login_log.py         # Login log
│   │   │   └── online.py            # Online user
│   │   │
│   │   ├── views/                    # API views
│   │   │   ├── __init__.py
│   │   │   ├── auth.py              # Login, logout, refresh
│   │   │   ├── user.py              # User CRUD
│   │   │   ├── role.py              # Role CRUD
│   │   │   ├── menu.py              # Menu CRUD
│   │   │   ├── dept.py              # Dept CRUD
│   │   │   ├── post.py              # Post CRUD
│   │   │   ├── dict.py              # Dict CRUD
│   │   │   ├── config.py            # Config CRUD
│   │   │   ├── oper_log.py          # Operation log
│   │   │   ├── login_log.py         # Login log
│   │   │   └── online.py            # Online users
│   │   │
│   │   ├── serializers/              # DRF serializers
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── role.py
│   │   │   ├── menu.py
│   │   │   ├── dept.py
│   │   │   └── ...
│   │   │
│   │   ├── services/                 # Business logic
│   │   │   ├── __init__.py
│   │   │   ├── auth.py              # Auth business logic
│   │   │   ├── permission.py        # Permission logic
│   │   │   └── data_scope.py        # Data scope logic
│   │   │
│   │   ├── filters/                  # Django filters
│   │   │   ├── __init__.py
│   │   │   └── user.py
│   │   │
│   │   ├── migrations/               # DB migrations
│   │   │   └── ...
│   │   │
│   │   └── urls.py                   # URL routing
│   │
│   ├── basic_data/                   # Basic data module
│   │   ├── __init__.py
│   │   ├── apps.py
│   │   │
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── client.py            # Client (客户)
│   │   │   ├── product.py           # Product (产品)
│   │   │   ├── procedure.py         # Procedure (工序)
│   │   │   ├── process_route.py     # Process route (工艺路线)
│   │   │   └── defect.py            # Defect (不良项)
│   │   │
│   │   ├── views/
│   │   │   ├── __init__.py
│   │   │   ├── client.py
│   │   │   ├── product.py
│   │   │   ├── procedure.py
│   │   │   ├── process_route.py
│   │   │   └── defect.py
│   │   │
│   │   ├── serializers/
│   │   │   └── ...
│   │   │
│   │   ├── migrations/
│   │   │   └── ...
│   │   │
│   │   └── urls.py
│   │
│   ├── production/                   # Production module
│   │   ├── __init__.py
│   │   ├── apps.py
│   │   │
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── sheet.py             # Work order (工单)
│   │   │   ├── task.py              # Task (任务)
│   │   │   └── job_booking.py       # Job booking (报工)
│   │   │
│   │   ├── views/
│   │   │   ├── __init__.py
│   │   │   ├── sheet.py
│   │   │   ├── task.py
│   │   │   └── job_booking.py
│   │   │
│   │   ├── serializers/
│   │   │   └── ...
│   │   │
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── sheet.py             # Sheet business logic
│   │   │   └── statistics.py        # Production statistics
│   │   │
│   │   ├── migrations/
│   │   │   └── ...
│   │   │
│   │   └── urls.py
│   │
│   ├── inventory/                    # Inventory module
│   │   ├── __init__.py
│   │   ├── apps.py
│   │   │
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── material.py          # Material (物料)
│   │   │   ├── supplier.py          # Supplier (供应商)
│   │   │   └── stock.py             # Stock operations
│   │   │
│   │   ├── views/
│   │   │   └── ...
│   │   │
│   │   ├── serializers/
│   │   │   └── ...
│   │   │
│   │   ├── migrations/
│   │   │   └── ...
│   │   │
│   │   └── urls.py
│   │
│   ├── report/                       # Report module
│   │   ├── __init__.py
│   │   ├── apps.py
│   │   │
│   │   ├── views/
│   │   │   ├── __init__.py
│   │   │   ├── production.py        # Production reports
│   │   │   ├── defect.py            # Defect analysis
│   │   │   └── inventory.py         # Inventory reports
│   │   │
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   └── statistics.py        # Statistics calculation
│   │   │
│   │   └── urls.py
│   │
│   └── monitor/                      # Monitor module
│       ├── __init__.py
│       ├── apps.py
│       │
│       ├── views/
│       │   ├── __init__.py
│       │   ├── cache.py             # Cache management
│       │   └── server.py            # Server info
│       │
│       └── urls.py
│
├── tenants/                          # Multi-tenant support
│   ├── __init__.py
│   ├── models.py                    # Tenant, TenantPackage
│   ├── middleware.py                # Tenant middleware
│   ├── schema.py                    # Schema utilities
│   └── migrations/
│       └── ...
│
├── tasks/                            # Celery tasks
│   ├── __init__.py
│   ├── celery.py                    # Celery app config
│   │
│   ├── scheduled/                    # Scheduled tasks
│   │   ├── __init__.py
│   │   ├── cleanup.py               # Cleanup tasks
│   │   └── report.py                # Report generation
│   │
│   └── async/                        # Async tasks
│       ├── __init__.py
│       ├── notification.py          # Notification tasks
│       └── export.py                # Export tasks
│
├── api/                              # API versioning
│   ├── __init__.py
│   │
│   └── v1/                           # API v1
│       ├── __init__.py
│       └── urls.py                  # v1 URL routing
│
├── tests/                            # Test suite
│   ├── __init__.py
│   ├── conftest.py                  # Pytest fixtures
│   │
│   ├── unit/                         # Unit tests
│   │   ├── __init__.py
│   │   ├── test_user.py
│   │   ├── test_role.py
│   │   └── ...
│   │
│   ├── integration/                  # Integration tests
│   │   ├── __init__.py
│   │   ├── test_auth.py
│   │   └── ...
│   │
│   └── factories/                    # Factory Boy factories
│       ├── __init__.py
│       └── user.py
│
├── scripts/                          # Utility scripts
│   ├── migrate_data.py              # Data migration from MySQL
│   ├── create_superuser.py          # Create superuser
│   └── generate_test_data.py        # Generate test data
│
├── docker/                           # Docker configuration
│   ├── Dockerfile
│   ├── Dockerfile.dev
│   ├── docker-compose.yml
│   ├── docker-compose.dev.yml
│   └── nginx.conf
│
├── docs/                             # Documentation
│   ├── api/                         # API documentation
│   ├── deployment/                  # Deployment guide
│   └── development/                 # Development guide
│
├── requirements/                     # Dependencies
│   ├── base.txt                     # Base dependencies
│   ├── development.txt              # Dev dependencies
│   ├── production.txt               # Prod dependencies
│   └── testing.txt                  # Test dependencies
│
├── static/                           # Static files
│   └── ...
│
├── media/                            # Media files
│   └── ...
│
├── locale/                           # Internationalization
│   └── ...
│
├── .env.example                      # Environment variables template
├── .gitignore
├── manage.py                         # Django management script
├── pyproject.toml                    # Project metadata
├── pytest.ini                        # Pytest configuration
├── Makefile                          # Make commands
└── README.md                         # Project README
```

---

## 2. Key Files Content

### 2.1 Settings Structure

```python
# config/settings/__init__.py

import os

env = os.environ.get('DJANGO_ENV', 'development')

if env == 'production':
    from .production import *
elif env == 'testing':
    from .testing import *
else:
    from .development import *
```

```python
# config/settings/base.py

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Core apps
DJANGO_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

# Third-party apps
THIRD_PARTY_APPS = [
    'rest_framework',
    'rest_framework_simplejwt',
    'django_filters',
    'django_tenants',
    'django_celery_beat',
    'corsheaders',
    'import_export',
]

# Local apps
LOCAL_APPS = [
    'apps.core',
    'apps.system',
    'apps.basic_data',
    'apps.production',
    'apps.inventory',
    'apps.report',
    'apps.monitor',
    'tenants',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'tenants.middleware.TenantMiddleware',
    'apps.core.middleware.request_logging.RequestLoggingMiddleware',
    'apps.core.middleware.exception_handler.ExceptionHandlerMiddleware',
]

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django_tenants.postgresql_backend',
        'NAME': 'cp_mes',
        'USER': 'postgres',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Redis Cache
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://localhost:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

# REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'EXCEPTION_HANDLER': 'apps.core.exceptions.custom_exception_handler',
}

# JWT Settings
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=2),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ALGORITHM': 'HS256',
    'AUTH_HEADER_TYPES': ('Bearer',),
}

# Celery
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
```

### 2.2 URL Configuration

```python
# config/urls.py

from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.system.views.auth import LoginView, LogoutView, RefreshView

router = DefaultRouter()

# System
router.registry.extend([
    # Will be populated by each app's urls.py
])

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Auth endpoints
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('refresh', RefreshView.as_view(), name='refresh'),
    
    # API v1
    path('api/v1/', include('api.v1.urls')),
    
    # API docs
    path('api/docs/', include('rest_framework.urls')),
]
```

```python
# api/v1/urls.py

from django.urls import path, include

urlpatterns = [
    path('system/', include('apps.system.urls')),
    path('basic/', include('apps.basic_data.urls')),
    path('production/', include('apps.production.urls')),
    path('inventory/', include('apps.inventory.urls')),
    path('report/', include('apps.report.urls')),
    path('monitor/', include('apps.monitor.urls')),
]
```

### 2.3 Requirements Files

```txt
# requirements/base.txt

# Django
Django==5.0
djangorestframework==3.14.0
django-cors-headers==4.3.1
django-filter==23.5

# Database
psycopg[binary]==3.1.18
django-tenants==3.6.1

# Authentication
djangorestframework-simplejwt==5.3.1
PyJWT==2.8.0

# Caching
django-redis==5.4.0
redis==5.0.1

# Task Queue
celery==5.3.6
django-celery-beat==2.5.0

# API Documentation
drf-spectacular==0.27.2

# Excel
openpyxl==3.1.2
django-import-export==4.0.5

# Utilities
orjson==3.9.12
python-dotenv==1.0.0
pydantic==2.5.0
```

```txt
# requirements/development.txt

-r base.txt

# Development tools
django-debug-toolbar==4.2.0
ipython==8.18.1
watchdog==3.0.0

# Testing
pytest==7.4.3
pytest-django==4.7.0
pytest-cov==4.1.0
factory-boy==3.3.0
```

```txt
# requirements/production.txt

-r base.txt

# Production server
gunicorn==21.2.0
uvicorn[standard]==0.27.0

# Security
django-ratelimit==4.1.0

# Monitoring
django-prometheus==2.3.1
structlog==24.1.0
```

### 2.4 Makefile

```makefile
# Makefile

.PHONY: help install dev run test clean migrate docker-up docker-down

help:
	@echo "Available commands:"
	@echo "  make install     - Install production dependencies"
	@echo "  make dev         - Install development dependencies"
	@echo "  make run         - Run development server"
	@echo "  make test        - Run tests"
	@echo "  make migrate     - Run database migrations"
	@echo "  make docker-up   - Start Docker containers"
	@echo "  make docker-down - Stop Docker containers"

install:
	pip install -r requirements/production.txt

dev:
	pip install -r requirements/development.txt

run:
	python manage.py runserver 0.0.0.0:8000

test:
	pytest tests/ -v --cov=apps

migrate:
	python manage.py makemigrations
	python manage.py migrate

docker-up:
	docker-compose -f docker/docker-compose.yml up -d

docker-down:
	docker-compose -f docker/docker-compose.yml down
```

---

## 3. Module Registration

```python
# apps/system/apps.py

from django.apps import AppConfig

class SystemConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.system'
    verbose_name = 'System Management'
```

```python
# apps/basic_data/apps.py

from django.apps import AppConfig

class BasicDataConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.basic_data'
    verbose_name = 'Basic Data'
```

```python
# apps/production/apps.py

from django.apps import AppConfig

class ProductionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.production'
    verbose_name = 'Production Management'
```

```python
# apps/inventory/apps.py

from django.apps import AppConfig

class InventoryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.inventory'
    verbose_name = 'Inventory Management'
```
