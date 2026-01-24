"""
User model
"""
from flask_login import UserMixin
from datetime import datetime
from app import db


class User(UserMixin, db.Model):
    """User model with role-based access control"""
    __tablename__ = 'users'
    
    # Roles
    ROLE_HEAD_CHEF = 'HEAD_CHEF'
    ROLE_CHEF = 'CHEF'
    ROLE_DELIVERY_PERSON = 'DELIVERY_PERSON'
    ROLE_ADMIN = 'ADMIN'
    ROLE_HEALTH_SAFETY_OFFICER = 'HEALTH_SAFETY_OFFICER'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False, index=True)
    email = db.Column(db.String(100), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    last_login = db.Column(db.DateTime, nullable=True)
    failed_login_attempts = db.Column(db.Integer, default=0, nullable=False)
    locked_until = db.Column(db.DateTime, nullable=True)
    
    # Relationships
    inventory_items = db.relationship('Inventory', backref='creator', lazy='dynamic')
    deliveries = db.relationship('Delivery', backref='delivery_person', lazy='dynamic')
    notifications = db.relationship('Notification', backref='user', lazy='dynamic')
    audit_logs = db.relationship('AuditLog', backref='user', lazy='dynamic')
    confirmed_reorders = db.relationship('Reorder', backref='confirmed_by_user', lazy='dynamic')
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    def is_locked(self):
        """Check if account is currently locked"""
        if self.locked_until:
            return datetime.utcnow() < self.locked_until
        return False
    
    def has_role(self, role):
        """Check if user has a specific role"""
        return self.role == role
    
    def is_head_chef(self):
        """Check if user is head chef"""
        return self.role == self.ROLE_HEAD_CHEF
    
    def is_admin(self):
        """Check if user is admin"""
        return self.role == self.ROLE_ADMIN
    
    def can_manage_users(self):
        """Check if user can manage other users"""
        return self.role in [self.ROLE_ADMIN, self.ROLE_HEAD_CHEF]
    
    def can_view_reports(self):
        """Check if user can view reports"""
        return self.role in [
            self.ROLE_ADMIN,
            self.ROLE_HEAD_CHEF,
            self.ROLE_HEALTH_SAFETY_OFFICER
        ]
