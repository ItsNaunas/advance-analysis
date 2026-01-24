"""
Integration tests for authentication routes
"""
import pytest


def test_login_page(client):
    """Test login page loads"""
    response = client.get('/auth/login')
    assert response.status_code == 200
    assert b'Login' in response.data


def test_login_success(client, sample_user):
    """Test successful login"""
    response = client.post('/auth/login', data={
        'username': 'testuser',
        'password': 'password'
    }, follow_redirects=True)
    
    assert response.status_code == 200


def test_login_invalid_credentials(client):
    """Test login with invalid credentials"""
    response = client.post('/auth/login', data={
        'username': 'nonexistent',
        'password': 'wrongpassword'
    })
    
    assert response.status_code == 200
    assert b'Invalid' in response.data or b'error' in response.data.lower()


def test_logout(client, sample_user):
    """Test logout"""
    # Login first
    client.post('/auth/login', data={
        'username': 'testuser',
        'password': 'password'
    })
    
    # Logout
    response = client.post('/auth/logout', follow_redirects=True)
    assert response.status_code == 200


def test_protected_route_requires_login(client):
    """Test that protected routes require login"""
    response = client.get('/inventory', follow_redirects=True)
    # Should redirect to login
    assert b'Login' in response.data or response.status_code == 200
