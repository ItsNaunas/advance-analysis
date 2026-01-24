"""
User repository - Data access for users
"""
from app import db
from app.models.user import User
from datetime import datetime, timedelta
from flask import current_app


class UserRepository:
    """Repository for user data access"""
    
    @staticmethod
    def get_by_id(user_id):
        """Get user by ID"""
        return User.query.get(user_id)
    
    @staticmethod
    def get_by_username(username):
        """Get user by username"""
        return User.query.filter_by(username=username).first()
    
    @staticmethod
    def get_by_email(email):
        """Get user by email"""
        return User.query.filter_by(email=email).first()
    
    @staticmethod
    def get_all():
        """Get all users"""
        return User.query.all()
    
    @staticmethod
    def get_by_role(role):
        """Get all users with specific role"""
        return User.query.filter_by(role=role).all()
    
    @staticmethod
    def create(username, email, password_hash, role):
        """Create new user"""
        user = User(
            username=username,
            email=email,
            password_hash=password_hash,
            role=role
        )
        db.session.add(user)
        db.session.commit()
        return user
    
    @staticmethod
    def update(user):
        """Update user"""
        db.session.commit()
        return user
    
    @staticmethod
    def delete(user):
        """Delete user"""
        db.session.delete(user)
        db.session.commit()
    
    @staticmethod
    def increment_failed_login(user):
        """Increment failed login attempts"""
        user.failed_login_attempts += 1
        max_attempts = current_app.config.get('MAX_LOGIN_ATTEMPTS', 3)
        lockout_duration = current_app.config.get('LOCKOUT_DURATION_MINUTES', 30)
        
        if user.failed_login_attempts >= max_attempts:
            user.locked_until = datetime.utcnow() + timedelta(minutes=lockout_duration)
        
        db.session.commit()
        return user
    
    @staticmethod
    def reset_failed_login(user):
        """Reset failed login attempts"""
        user.failed_login_attempts = 0
        user.locked_until = None
        db.session.commit()
        return user
    
    @staticmethod
    def update_last_login(user):
        """Update last login timestamp"""
        user.last_login = datetime.utcnow()
        db.session.commit()
        return user
