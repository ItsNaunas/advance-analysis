"""
Test delivery routes
"""
import pytest
from flask import url_for
from app.models.delivery import Delivery
from app.models.user import User


def test_new_delivery_page_requires_login(client):
    """Test new delivery page requires authentication"""
    response = client.get('/deliveries/new')
    assert response.status_code == 302  # Redirect to login


def test_new_delivery_page_requires_delivery_role(client, sample_chef):
    """Test new delivery page requires DELIVERY_PERSON role"""
    # Login as chef (not delivery person)
    client.post('/auth/login', data={
        'username': sample_chef.username,
        'password': 'password123'
    })
    
    response = client.get('/deliveries/new')
    assert response.status_code == 403  # Forbidden due to insufficient permissions


def test_new_delivery_page_accessible_to_delivery_person(client, sample_delivery_person):
    """Test new delivery page accessible to delivery person"""
    # Login as delivery person
    client.post('/auth/login', data={
        'username': sample_delivery_person.username,
        'password': 'password123'
    })
    
    response = client.get('/deliveries/new')
    assert response.status_code == 200
    assert b'New Delivery' in response.data


def test_submit_delivery_success(client, sample_delivery_person, app):
    """Test successful delivery submission with auto-populated fields"""
    # Login as delivery person
    client.post('/auth/login', data={
        'username': sample_delivery_person.username,
        'password': 'password123'
    })
    
    # Submit delivery
    response = client.post('/deliveries/submit',
                          json={
                              'items': [
                                  {'item_name': 'Tomatoes', 'quantity': 10},
                                  {'item_name': 'Cheese', 'quantity': 5}
                              ]
                          })
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert 'delivery_id' in data
    assert data['delivery_person'] == sample_delivery_person.username
    assert 'date' in data
    
    # Verify delivery was created with auto-populated fields
    with app.app_context():
        delivery = Delivery.query.get(data['delivery_id'])
        assert delivery is not None
        assert delivery.delivery_person_id == sample_delivery_person.id  # Auto-populated
        assert delivery.scheduled_date is not None  # Auto-populated
        assert delivery.created_at is not None  # Auto-populated
        assert len(delivery.items) == 2
        assert delivery.items[0]['item_name'] == 'Tomatoes'
        assert delivery.items[0]['quantity'] == 10
        assert delivery.items[1]['item_name'] == 'Cheese'
        assert delivery.items[1]['quantity'] == 5


def test_submit_delivery_no_items(client, sample_delivery_person):
    """Test delivery submission fails with no items"""
    # Login as delivery person
    client.post('/auth/login', data={
        'username': sample_delivery_person.username,
        'password': 'password123'
    })
    
    # Submit delivery with no items
    response = client.post('/deliveries/submit',
                          json={'items': []})
    
    assert response.status_code == 400
    data = response.get_json()
    assert data['success'] is False


def test_submit_delivery_requires_login(client):
    """Test delivery submission requires authentication"""
    response = client.post('/deliveries/submit',
                          json={
                              'items': [
                                  {'item_name': 'Tomatoes', 'quantity': 10}
                              ]
                          })
    assert response.status_code == 302  # Redirect to login


def test_submit_delivery_requires_delivery_role(client, sample_chef):
    """Test delivery submission requires DELIVERY_PERSON role"""
    # Login as chef (not delivery person)
    client.post('/auth/login', data={
        'username': sample_chef.username,
        'password': 'password123'
    })
    
    response = client.post('/deliveries/submit',
                          json={
                              'items': [
                                  {'item_name': 'Tomatoes', 'quantity': 10}
                              ]
                          })
    assert response.status_code == 403  # Forbidden due to insufficient permissions


def test_delivery_dashboard_has_new_delivery_button(client, sample_delivery_person):
    """Test delivery person dashboard has New Delivery button"""
    # Login as delivery person
    client.post('/auth/login', data={
        'username': sample_delivery_person.username,
        'password': 'password123'
    })
    
    response = client.get('/dashboard/delivery-person')
    assert response.status_code == 200
    assert b'New Delivery' in response.data
    assert b'href="/deliveries/new"' in response.data
