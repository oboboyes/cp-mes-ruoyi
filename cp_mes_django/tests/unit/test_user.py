"""
Tests for user API.
"""

import pytest
from rest_framework.test import APIClient
from django.urls import reverse


class TestUserAPI:
    """
    Test user API.
    """
    
    def test_list_users_authenticated(self, authenticated_client):
        """
        Test list users when authenticated.
        """
        url = reverse('user-list')
        response = authenticated_client.get(url)
        
        assert response.status_code == 200
        assert response.data['code'] == 200
    
    def test_list_users_unauthenticated(self, api_client):
        """
        Test list users when not authenticated.
        """
        url = reverse('user-list')
        response = api_client.get(url)
        
        assert response.status_code == 401
    
    def test_create_user(self, authenticated_client):
        """
        Test create user.
        """
        url = reverse('user-list')
        data = {
            'username': 'newuser',
            'nick_name': 'New User',
            'password': 'newpassword123',
            'email': 'newuser@example.com',
            'phonenumber': '13800138000',
            'sex': '0',
            'status': '0'
        }
        response = authenticated_client.post(url, data, format='json')
        
        assert response.status_code == 201
        assert response.data['code'] == 200
    
    def test_get_user_detail(self, authenticated_client, test_user):
        """
        Test get user detail.
        """
        url = reverse('user-detail', kwargs={'pk': test_user.id})
        response = authenticated_client.get(url)
        
        assert response.status_code == 200
        assert response.data['code'] == 200
    
    def test_update_user(self, authenticated_client, test_user):
        """
        Test update user.
        """
        url = reverse('user-detail', kwargs={'pk': test_user.id})
        data = {
            'nick_name': 'Updated Name',
            'email': 'updated@example.com'
        }
        response = authenticated_client.patch(url, data, format='json')
        
        assert response.status_code == 200
        assert response.data['code'] == 200
    
    def test_delete_user(self, authenticated_client, test_user):
        """
        Test delete user (soft delete).
        """
        # Create another user to delete
        from apps.system.models import User
        user_to_delete = User.objects.create_user(
            username='todelete',
            password='password123',
            nick_name='To Delete'
        )
        
        url = reverse('user-detail', kwargs={'pk': user_to_delete.id})
        response = authenticated_client.delete(url)
        
        assert response.status_code == 204
        
        # Verify soft delete
        user_to_delete.refresh_from_db()
        assert user_to_delete.del_flag == '2'
    
    def test_reset_password(self, authenticated_client, test_user):
        """
        Test reset password.
        """
        url = reverse('user-reset-password', kwargs={'pk': test_user.id})
        data = {'password': 'newpassword123'}
        response = authenticated_client.put(url, data, format='json')
        
        assert response.status_code == 200
        assert response.data['code'] == 200
    
    def test_change_status(self, authenticated_client, test_user):
        """
        Test change user status.
        """
        url = reverse('user-change-status', kwargs={'pk': test_user.id})
        data = {'status': '1'}
        response = authenticated_client.put(url, data, format='json')
        
        assert response.status_code == 200
        assert response.data['code'] == 200
