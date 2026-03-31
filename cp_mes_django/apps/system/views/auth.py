"""
Authentication views for cp_mes project.
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.conf import settings

from apps.system.models import User, LoginLog
from apps.core.utils.request import get_client_ip, get_user_agent
from apps.core.authentication import create_tokens_for_user


class LoginView(APIView):
    """
    User login view.
    """
    permission_classes = []
    
    def post(self, request):
        """
        User login.
        """
        username = request.data.get('username')
        password = request.data.get('password')
        code = request.data.get('code')  # Captcha code
        uuid = request.data.get('uuid')  # Captcha UUID
        
        # Validate input
        if not username or not password:
            return Response({
                'code': 400,
                'msg': '用户名和密码不能为空',
                'data': None
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # TODO: Validate captcha if enabled
        # if settings.CAPTCHA_ENABLED:
        #     if not self.validate_captcha(code, uuid):
        #         return Response({'code': 400, 'msg': '验证码错误', 'data': None})
        
        # Authenticate user
        user = authenticate(request, username=username, password=password)
        
        if user is None:
            # Log failed login
            self.log_login(request, username, '1', '用户名或密码错误')
            return Response({
                'code': 401,
                'msg': '用户名或密码错误',
                'data': None
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        if not user.is_active:
            self.log_login(request, username, '1', '账号已被停用')
            return Response({
                'code': 401,
                'msg': '账号已被停用',
                'data': None
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        if user.status != '0':
            self.log_login(request, username, '1', '账号已被停用')
            return Response({
                'code': 401,
                'msg': '账号已被停用',
                'data': None
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        # Generate tokens
        tokens = create_tokens_for_user(user)
        
        # Update login info
        user.login_ip = get_client_ip(request)
        user.login_date = user._meta.model.objects.filter(pk=user.pk).values_list('create_time', flat=True).first()
        user.save(update_fields=['login_ip', 'login_date'])
        
        # Log successful login
        self.log_login(request, username, '0', '登录成功', user.tenant_id)
        
        return Response({
            'code': 200,
            'msg': '登录成功',
            'data': {
                'token': tokens['access'],
                'refreshToken': tokens['refresh'],
            }
        })
    
    def log_login(self, request, username, status, msg, tenant_id=None):
        """
        Log login attempt.
        """
        ip = get_client_ip(request)
        user_agent = get_user_agent(request)
        
        # Parse browser and OS from user agent
        browser = 'Unknown'
        os_name = 'Unknown'
        if 'Chrome' in user_agent:
            browser = 'Chrome'
        elif 'Firefox' in user_agent:
            browser = 'Firefox'
        elif 'Safari' in user_agent:
            browser = 'Safari'
        elif 'Edge' in user_agent:
            browser = 'Edge'
        
        if 'Windows' in user_agent:
            os_name = 'Windows'
        elif 'Mac' in user_agent:
            os_name = 'Mac'
        elif 'Linux' in user_agent:
            os_name = 'Linux'
        elif 'Android' in user_agent:
            os_name = 'Android'
        elif 'iOS' in user_agent:
            os_name = 'iOS'
        
        LoginLog.create_log(
            username=username,
            ip=ip,
            location='',  # Can be filled with IP location lookup
            browser=browser,
            os=os_name,
            status=status,
            msg=msg,
            tenant_id=tenant_id
        )


class LogoutView(APIView):
    """
    User logout view.
    """
    
    def post(self, request):
        """
        User logout.
        """
        # JWT tokens are stateless, so we just return success
        # In production, you might want to blacklist the token
        return Response({
            'code': 200,
            'msg': '退出成功',
            'data': None
        })


class RefreshView(APIView):
    """
    Token refresh view.
    """
    permission_classes = []
    
    def post(self, request):
        """
        Refresh access token.
        """
        refresh_token = request.data.get('refreshToken')
        
        if not refresh_token:
            return Response({
                'code': 400,
                'msg': '刷新令牌不能为空',
                'data': None
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)
            
            return Response({
                'code': 200,
                'msg': '刷新成功',
                'data': {
                    'token': access_token,
                }
            })
        except Exception as e:
            return Response({
                'code': 401,
                'msg': '刷新令牌无效或已过期',
                'data': None
            }, status=status.HTTP_401_UNAUTHORIZED)


class GetInfoView(APIView):
    """
    Get current user info view.
    """
    
    def get(self, request):
        """
        Get current user info.
        """
        user = request.user
        
        # Get roles
        roles = user.roles.filter(status='0', del_flag='0').values_list('role_key', flat=True)
        role_keys = list(roles) if not user.is_superuser else ['admin']
        
        # Get permissions
        permissions = user.get_all_permissions()
        if user.is_superuser:
            permissions = ['*:*:*']
        
        return Response({
            'code': 200,
            'msg': '获取成功',
            'data': {
                'user': {
                    'userId': user.id,
                    'userName': user.username,
                    'nickName': user.nick_name,
                    'deptId': user.dept_id,
                    'email': user.email,
                    'phonenumber': user.phonenumber,
                    'sex': user.sex,
                    'avatar': user.avatar,
                    'status': user.status,
                },
                'roles': role_keys,
                'permissions': list(permissions),
            }
        })
