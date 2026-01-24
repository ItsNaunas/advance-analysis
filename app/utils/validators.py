"""
Validation utilities
"""
from datetime import date, datetime
from flask import current_app


def validate_email(email):
    """Basic email validation"""
    if not email or '@' not in email:
        return False
    return len(email) <= 100


def validate_username(username):
    """Validate username"""
    if not username:
        return False
    if len(username) < 3 or len(username) > 50:
        return False
    # Only alphanumeric and underscore
    return username.replace('_', '').isalnum()


def validate_password(password):
    """Validate password strength"""
    if not password:
        return False
    if len(password) < 6:
        return False
    return True


def validate_date(date_string):
    """Validate date string"""
    try:
        datetime.strptime(date_string, '%Y-%m-%d')
        return True
    except (ValueError, TypeError):
        return False


def validate_quantity(quantity):
    """Validate quantity"""
    try:
        qty = int(quantity)
        return qty >= 0
    except (ValueError, TypeError):
        return False


def validate_role(role):
    """Validate user role"""
    valid_roles = [
        'HEAD_CHEF',
        'CHEF',
        'DELIVERY_PERSON',
        'ADMIN',
        'HEALTH_SAFETY_OFFICER'
    ]
    return role in valid_roles
