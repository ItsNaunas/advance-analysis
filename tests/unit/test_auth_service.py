"""
Unit tests for authentication service
"""
import pytest
from app.services.auth_service import AuthService
from app.repositories.user_repository import UserRepository
from app.utils.password_hasher import verify_password


def test_authenticate_success(app, sample_user):
    """Test successful authentication"""
    with app.app_context():
        auth_service = AuthService()
        user, error = auth_service.authenticate('testuser', 'password')
        
        assert user is not None
        assert error is None
        assert user.username == 'testuser'


def test_authenticate_invalid_password(app, sample_user):
    """Test authentication with invalid password"""
    with app.app_context():
        auth_service = AuthService()
        user, error = auth_service.authenticate('testuser', 'wrongpassword')
        
        assert user is None
        assert error is not None


def test_authenticate_invalid_username(app):
    """Test authentication with invalid username"""
    with app.app_context():
        auth_service = AuthService()
        user, error = auth_service.authenticate('nonexistent', 'password')
        
        assert user is None
        assert error is not None


def test_create_user_success(app):
    """Test successful user creation"""
    with app.app_context():
        auth_service = AuthService()
        user, error = auth_service.create_user(
            'newuser', 'newuser@example.com', 'password123', 'CHEF'
        )
        
        assert user is not None
        assert error is None
        assert user.username == 'newuser'
        assert verify_password('password123', user.password_hash)


def test_create_user_duplicate_username(app, sample_user):
    """Test user creation with duplicate username"""
    with app.app_context():
        auth_service = AuthService()
        user, error = auth_service.create_user(
            'testuser', 'different@example.com', 'password123', 'CHEF'
        )
        
        assert user is None
        assert error is not None
        assert 'already exists' in error.lower()


def test_create_user_invalid_password(app):
    """Test user creation with invalid password"""
    with app.app_context():
        auth_service = AuthService()
        user, error = auth_service.create_user(
            'newuser', 'newuser@example.com', '123', 'CHEF'
        )
        
        assert user is None
        assert error is not None
