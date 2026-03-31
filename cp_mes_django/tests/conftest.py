"""
Pytest configuration for cp_mes project.
"""

import pytest
import os
import django

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.testing')

# Setup Django
django.setup()


@pytest.fixture(scope='session')
def django_db_setup():
    """
    Database setup for tests.
    """
    from django.conf import settings
    settings.DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }


@pytest.fixture
def api_client():
    """
    API client for testing.
    """
    from rest_framework.test import APIClient
    return APIClient()


@pytest.fixture
def test_user(db):
    """
    Create a test user.
    """
    from apps.system.models import User
    user = User.objects.create_user(
        username='testuser',
        password='testpassword123',
        nick_name='Test User',
        email='test@example.com',
    )
    return user


@pytest.fixture
def authenticated_client(api_client, test_user):
    """
    Authenticated API client.
    """
    from apps.core.authentication import create_tokens_for_user
    
    tokens = create_tokens_for_user(test_user)
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {tokens["access"]}')
    return api_client


@pytest.fixture
def admin_user(db):
    """
    Create an admin user.
    """
    from apps.system.models import User
    user = User.objects.create_superuser(
        username='admin',
        password='adminpassword123',
        nick_name='Admin User',
    )
    return user
