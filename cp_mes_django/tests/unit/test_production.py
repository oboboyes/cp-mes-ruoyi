"""
Tests for production API.
"""

import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from decimal import Decimal
from datetime import datetime

from apps.production.models import Sheet, Task, JobBooking
from apps.basic_data.models import Product


@pytest.fixture
def test_product(db):
    """Create a test product."""
    return Product.objects.create(
        product_code='PROD001',
        product_name='Test Product',
        status='0'
    )


@pytest.fixture
def test_sheet(db, test_product):
    """Create a test sheet."""
    return Sheet.objects.create(
        sheet_code='SHEET001',
        sheet_name='Test Work Order',
        product_id=test_product.id,
        product_name=test_product.name,
        quantity=Decimal('100.00'),
        status='0'
    )


class TestSheetAPI:
    """
    Test sheet (work order) API.
    """
    
    def test_list_sheets(self, authenticated_client):
        """
        Test list sheets.
        """
        url = reverse('sheet-list')
        response = authenticated_client.get(url)
        
        assert response.status_code == 200
        assert response.data['code'] == 200
    
    def test_create_sheet(self, authenticated_client, test_product):
        """
        Test create sheet.
        """
        url = reverse('sheet-list')
        data = {
            'sheet_code': 'SHEET002',
            'sheet_name': 'New Work Order',
            'product_id': test_product.id,
            'product_name': test_product.product_name,
            'quantity': '50.00'
        }
        response = authenticated_client.post(url, data, format='json')
        
        assert response.status_code == 201
        assert response.data['code'] == 200
    
    def test_start_production(self, authenticated_client, test_sheet):
        """
        Test start production.
        """
        url = reverse('sheet-start', kwargs={'pk': test_sheet.id})
        response = authenticated_client.put(url)
        
        assert response.status_code == 200
        assert response.data['code'] == 200
        
        test_sheet.refresh_from_db()
        assert test_sheet.status == '1'
    
    def test_complete_production(self, authenticated_client, test_sheet):
        """
        Test complete production.
        """
        # First start production
        test_sheet.status = '1'
        test_sheet.save()
        
        url = reverse('sheet-complete', kwargs={'pk': test_sheet.id})
        response = authenticated_client.put(url)
        
        assert response.status_code == 200
        assert response.data['code'] == 200
        
        test_sheet.refresh_from_db()
        assert test_sheet.status == '2'
    
    def test_cancel_work_order(self, authenticated_client, test_sheet):
        """
        Test cancel work order.
        """
        url = reverse('sheet-cancel', kwargs={'pk': test_sheet.id})
        response = authenticated_client.put(url)
        
        assert response.status_code == 200
        assert response.data['code'] == 200
        
        test_sheet.refresh_from_db()
        assert test_sheet.status == '3'


class TestTaskAPI:
    """
    Test task API.
    """
    
    def test_list_tasks(self, authenticated_client):
        """
        Test list tasks.
        """
        url = reverse('task-list')
        response = authenticated_client.get(url)
        
        assert response.status_code == 200
        assert response.data['code'] == 200


class TestJobBookingAPI:
    """
    Test job booking API.
    """
    
    def test_list_job_bookings(self, authenticated_client):
        """
        Test list job bookings.
        """
        url = reverse('job-booking-list')
        response = authenticated_client.get(url)
        
        assert response.status_code == 200
        assert response.data['code'] == 200
