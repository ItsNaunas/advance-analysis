"""
Role-Based Access Control middleware
"""
from functools import wraps
from flask import abort, redirect, url_for, flash
from flask_login import current_user


def require_role(*roles):
    """Decorator to require specific role(s)"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect(url_for('auth.login'))
            if current_user.role not in roles:
                flash('You do not have permission to access this page.', 'error')
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def require_authenticated(f):
    """Decorator to require authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function


def require_head_chef_or_admin(f):
    """Decorator to require Head Chef or Admin role"""
    return require_role('HEAD_CHEF', 'ADMIN')(f)


def require_admin(f):
    """Decorator to require Admin role"""
    return require_role('ADMIN')(f)
