"""
Monitor views for cp_mes project.
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.cache import cache
from django.db import connection
from django.conf import settings
import psutil
import time

from apps.core.permissions import IsAuthenticated, IsAdminUser
from apps.system.models import User, OperLog, LoginLog


class CacheInfoView(APIView):
    """
    Cache info view.
    """
    permission_classes = [IsAdminUser]
    
    def get(self, request):
        """
        Get cache information.
        """
        try:
            # Get Redis info
            info = cache.client.get_client().info()
            
            return Response({
                'code': 200,
                'msg': '获取成功',
                'data': {
                    'usedMemory': info.get('used_memory_human', 'N/A'),
                    'totalKeys': info.get('keyspace_hits', 0),
                    'hits': info.get('keyspace_hits', 0),
                    'misses': info.get('keyspace_misses', 0),
                    'uptime': info.get('uptime_in_seconds', 0),
                }
            })
        except Exception as e:
            return Response({
                'code': 500,
                'msg': f'获取缓存信息失败: {str(e)}',
                'data': None
            })
    
    def delete(self, request):
        """
        Clear all cache.
        """
        try:
            cache.clear()
            return Response({
                'code': 200,
                'msg': '缓存清理成功',
                'data': None
            })
        except Exception as e:
            return Response({
                'code': 500,
                'msg': f'缓存清理失败: {str(e)}',
                'data': None
            })


class ServerInfoView(APIView):
    """
    Server info view.
    """
    permission_classes = [IsAdminUser]
    
    def get(self, request):
        """
        Get server information.
        """
        try:
            # CPU info
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_count = psutil.cpu_count()
            
            # Memory info
            memory = psutil.virtual_memory()
            
            # Disk info
            disk = psutil.disk_usage('/')
            
            # Network info
            network = psutil.net_io_counters()
            
            return Response({
                'code': 200,
                'msg': '获取成功',
                'data': {
                    'cpu': {
                        'percent': cpu_percent,
                        'count': cpu_count,
                    },
                    'memory': {
                        'total': memory.total,
                        'used': memory.used,
                        'percent': memory.percent,
                        'available': memory.available,
                    },
                    'disk': {
                        'total': disk.total,
                        'used': disk.used,
                        'percent': disk.percent,
                        'free': disk.free,
                    },
                    'network': {
                        'bytesSent': network.bytes_sent,
                        'bytesRecv': network.bytes_recv,
                    }
                }
            })
        except Exception as e:
            return Response({
                'code': 500,
                'msg': f'获取服务器信息失败: {str(e)}',
                'data': None
            })


class DatabaseInfoView(APIView):
    """
    Database info view.
    """
    permission_classes = [IsAdminUser]
    
    def get(self, request):
        """
        Get database information.
        """
        try:
            with connection.cursor() as cursor:
                # Get database size
                cursor.execute("SELECT pg_database_size(current_database())")
                db_size = cursor.fetchone()[0]
                
                # Get table count
                cursor.execute("""
                    SELECT count(*) 
                    FROM information_schema.tables 
                    WHERE table_schema = 'public'
                """)
                table_count = cursor.fetchone()[0]
                
                # Get connection count
                cursor.execute("SELECT count(*) FROM pg_stat_activity")
                connection_count = cursor.fetchone()[0]
            
            return Response({
                'code': 200,
                'msg': '获取成功',
                'data': {
                    'databaseSize': db_size,
                    'tableCount': table_count,
                    'connectionCount': connection_count,
                }
            })
        except Exception as e:
            return Response({
                'code': 500,
                'msg': f'获取数据库信息失败: {str(e)}',
                'data': None
            })


class OnlineUserView(APIView):
    """
    Online user view.
    """
    permission_classes = [IsAdminUser]
    
    def get(self, request):
        """
        Get online users.
        """
        try:
            # Get online users from cache
            online_users = cache.get('online_users', [])
            
            return Response({
                'code': 200,
                'msg': '获取成功',
                'data': online_users
            })
        except Exception as e:
            return Response({
                'code': 500,
                'msg': f'获取在线用户失败: {str(e)}',
                'data': None
            })
    
    def delete(self, request):
        """
        Force user offline.
        """
        user_id = request.data.get('userId')
        if not user_id:
            return Response({
                'code': 400,
                'msg': '用户ID不能为空',
                'data': None
            })
        
        try:
            # Remove user from online list
            online_users = cache.get('online_users', [])
            online_users = [u for u in online_users if u.get('userId') != user_id]
            cache.set('online_users', online_users)
            
            return Response({
                'code': 200,
                'msg': '强制下线成功',
                'data': None
            })
        except Exception as e:
            return Response({
                'code': 500,
                'msg': f'强制下线失败: {str(e)}',
                'data': None
            })


class SystemStatsView(APIView):
    """
    System statistics view.
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """
        Get system statistics.
        """
        try:
            # User count
            user_count = User.objects.filter(del_flag='0').count()
            
            # Today's login count
            from django.utils import timezone
            today = timezone.now().date()
            today_login_count = LoginLog.objects.filter(
                login_time__date=today,
                status='0'
            ).count()
            
            # Today's operation count
            today_oper_count = OperLog.objects.filter(
                oper_time__date=today
            ).count()
            
            return Response({
                'code': 200,
                'msg': '获取成功',
                'data': {
                    'userCount': user_count,
                    'todayLoginCount': today_login_count,
                    'todayOperCount': today_oper_count,
                }
            })
        except Exception as e:
            return Response({
                'code': 500,
                'msg': f'获取系统统计失败: {str(e)}',
                'data': None
            })
