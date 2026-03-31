"""
JWT authentication components.
"""

from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomAccessToken(RefreshToken):
    """
    Custom JWT access token with additional claims.
    """
    
    @classmethod
    def for_user(cls, user):
        """
        Create token with custom claims.
        """
        token = super().for_user(user)
        
        # Add custom claims
        token['user_id'] = user.id
        token['username'] = user.username
        
        # Add department
        if hasattr(user, 'dept_id'):
            token['dept_id'] = user.dept_id
        
        # Add roles
        if hasattr(user, 'roles'):
            token['roles'] = list(user.roles.values_list('role_key', flat=True))
        
        # Add tenant
        if hasattr(user, 'tenant_id'):
            token['tenant_id'] = user.tenant_id
        
        return token


class JWTAuthenticationBackend(ModelBackend):
    """
    Custom authentication backend for JWT.
    """
    
    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        Authenticate user by username and password.
        """
        try:
            user = User.objects.get(username=username)
            if user.check_password(password) and user.is_active:
                return user
        except User.DoesNotExist:
            return None
        
        return None
    
    def get_user(self, user_id):
        """
        Get user by ID.
        """
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


def create_tokens_for_user(user):
    """
    Create access and refresh tokens for a user.
    """
    refresh = CustomAccessToken.for_user(user)
    return {
        'access': str(refresh.access_token),
        'refresh': str(refresh),
    }


def get_user_from_token(token):
    """
    Get user from JWT token.
    """
    try:
        from rest_framework_simplejwt.tokens import AccessToken
        access_token = AccessToken(token)
        user_id = access_token['user_id']
        return User.objects.get(id=user_id)
    except Exception:
        return None
