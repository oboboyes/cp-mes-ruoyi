"""
URL configuration for cp_mes project.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse

from apps.system.views.auth import LoginView, LogoutView, RefreshView, GetInfoView


def api_index(request):
    """API index endpoint showing available endpoints."""
    return JsonResponse({
        'message': 'CP-MES API Server',
        'version': '1.0.0',
        'endpoints': {
            'auth': {
                'login': '/login',
                'logout': '/logout',
                'refresh': '/refresh',
                'getInfo': '/getInfo',
            },
            'modules': {
                'system': '/system/',
                'basic': '/basic/',
                'production': '/production/',
                'inventory': '/inventory/',
                'report': '/report/',
                'monitor': '/monitor/',
            },
            'admin': '/admin/',
        }
    })


urlpatterns = [
    # API Index
    path('', api_index, name='api_index'),
    
    # Admin
    path('admin/', admin.site.urls),
    
    # Authentication endpoints
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('refresh', RefreshView.as_view(), name='refresh'),
    path('getInfo', GetInfoView.as_view(), name='get_info'),
    
    # API v1 modules
    path('system/', include('apps.system.urls')),
    path('basic/', include('apps.basic_data.urls')),
    path('production/', include('apps.production.urls')),
    path('inventory/', include('apps.inventory.urls')),
    path('report/', include('apps.report.urls')),
    path('monitor/', include('apps.monitor.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
    # Debug toolbar
    try:
        import debug_toolbar
        urlpatterns = [
            path('__debug__/', include(debug_toolbar.urls)),
        ] + urlpatterns
    except ImportError:
        pass
