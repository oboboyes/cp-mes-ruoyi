"""
Tests for authentication.
"""

import pytest
from rest_framework.test import APIClient
from django.urls import reverse


class TestAuthAPI:
    """
    Test authentication API.
    """
    
    def test_login_success(self, api_client, test_user):
        """
        Test successful login.
        """
        url = reverse('login')
        data = {
            'username': 'testuser',
            'password': 'testpassword123'
        }
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == 200
        assert response.data['code'] == 200
        assert 'token' in response.data['data']
    
    def test_login_invalid_password(self, api_client, test_user):
        """
        Test login with invalid password.
        """
        url = reverse('login')
        data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == 401
        assert response.data['code'] == 401
    
    def test_login_missing_fields(self, api_client):
        """
        Test login with missing fields.
        """
        url = reverse('login')
        data = {'username': 'testuser'}
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == 400
        assert response.data['code'] == 400
    
    def test_get_info_authenticated(self, authenticated_client):
        """
        Test get user info when authenticated.
        """
        url = reverse('get_info')
        response = authenticated_client.get(url)
        
        assert response.status_code == 200
        assert response.data['code'] == 200
        assert 'user' in response.data['data']
        assert 'roles' in response.data['data']
        assert 'permissions' in response.data['data']
    
    def test_get_info_unauthenticated(self, api_client):
        """
        Test get user info when not authenticated.
        """
        url = reverse('get_info')
        response = api_client.get(url)
        
        assert response.status_code == 401
    
    def test_logout(self, authenticated_client):
        """
        Test logout.
        """
        url = reverse('logout')
        response = authenticated_client.post(url)
        
        assert response.status_code == 200
        assert response.data['code'] == 200
    
    def test_refresh_token(self, api_client, test_user):
        """
        Test refresh token.
        """
        # First login to get refresh token
        from apps.core.authentication import create_tokens_for_user
        tokens = create_tokens_for_user(test_user)
        
        url = reverse('refresh')
        data = {'refreshToken': tokens['refresh']}
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == 200
        assert 'token' in response.data['data']
