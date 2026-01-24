"""
Authentication service - Business logic for authentication
"""
from app.repositories.user_repository import UserRepository
from app.utils.password_hasher import hash_password, verify_password
from app.utils.validators import validate_username, validate_email, validate_password, validate_role
from app.models.audit_log import AuditLog
from app import db
from flask import current_app


class AuthService:
    """Service for authentication operations"""
    
    def __init__(self):
        self.user_repo = UserRepository()
    
    def authenticate(self, username, password):
        """Authenticate user with username and password"""
        user = self.user_repo.get_by_username(username)
        
        if not user:
            return None, "Invalid username or password"
        
        # Check if account is locked
        if user.is_locked():
            return None, "Account is locked. Please try again later."
        
        # Verify password
        if not verify_password(password, user.password_hash):
            # Increment failed attempts
            self.user_repo.increment_failed_login(user)
            AuditLog.log_action(None, 'LOGIN_FAILED', 'USER', user.id, {'username': username})
            return None, "Invalid username or password"
        
        # Reset failed attempts on successful login
        self.user_repo.reset_failed_login(user)
        self.user_repo.update_last_login(user)
        AuditLog.log_action(user.id, 'LOGIN_SUCCESS', 'USER', user.id, {'username': username})
        
        return user, None
    
    def create_user(self, username, email, password, role):
        """Create new user"""
        # Validate inputs
        if not validate_username(username):
            return None, "Invalid username"
        
        if not validate_email(email):
            return None, "Invalid email"
        
        if not validate_password(password):
            return None, "Password must be at least 6 characters"
        
        if not validate_role(role):
            return None, "Invalid role"
        
        # Check if username exists
        if self.user_repo.get_by_username(username):
            return None, "Username already exists"
        
        # Check if email exists
        if self.user_repo.get_by_email(email):
            return None, "Email already exists"
        
        # Hash password
        password_hash = hash_password(password)
        
        # Create user
        user = self.user_repo.create(username, email, password_hash, role)
        AuditLog.log_action(None, 'USER_CREATED', 'USER', user.id, {'username': username, 'role': role})
        
        return user, None
    
    def change_password(self, user, old_password, new_password):
        """Change user password"""
        # Verify old password
        if not verify_password(old_password, user.password_hash):
            return False, "Current password is incorrect"
        
        # Validate new password
        if not validate_password(new_password):
            return False, "New password must be at least 6 characters"
        
        # Update password
        user.password_hash = hash_password(new_password)
        self.user_repo.update(user)
        AuditLog.log_action(user.id, 'PASSWORD_CHANGED', 'USER', user.id, {})
        
        return True, None
