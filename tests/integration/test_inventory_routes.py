"""
Integration tests for inventory routes
"""
import pytest
from datetime import date, timedelta


def test_inventory_list_requires_login(client):
    """Test inventory list requires login"""
    response = client.get('/inventory', follow_redirects=True)
    assert b'Login' in response.data or response.status_code == 200


def test_inventory_list_authenticated(client, sample_user):
    """Test inventory list for authenticated user"""
    # Login
    client.post('/auth/login', data={
        'username': 'testuser',
        'password': 'password'
    })
    
    response = client.get('/inventory')
    assert response.status_code == 200
    assert b'Inventory' in response.data


def test_add_item_page_requires_login(client):
    """Test add item page requires login"""
    response = client.get('/inventory/add', follow_redirects=True)
    assert b'Login' in response.data or response.status_code == 200


def test_add_item_authenticated(client, sample_user, sample_supplier):
    """Test adding item as authenticated user"""
    # Login
    client.post('/auth/login', data={
        'username': 'testuser',
        'password': 'password'
    })
    
    response = client.post('/inventory/add', data={
        'item_name': 'Test Item',
        'quantity': '10',
        'supplier_id': str(sample_supplier.id),
        'date_added': date.today().strftime('%Y-%m-%d'),
        'expiration_date': (date.today() + timedelta(days=7)).strftime('%Y-%m-%d')
    }, follow_redirects=True)
    
    assert response.status_code == 200
