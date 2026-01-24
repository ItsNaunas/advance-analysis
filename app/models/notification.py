"""
Notification model
"""
from datetime import datetime
from app import db


class Notification(db.Model):
    """Notification model"""
    __tablename__ = 'notifications'
    
    # Notification types
    TYPE_EXPIRY_WARNING = 'EXPIRY_WARNING'
    TYPE_LOW_STOCK = 'LOW_STOCK'
    TYPE_REORDER_READY = 'REORDER_READY'
    TYPE_DELIVERY_SCHEDULED = 'DELIVERY_SCHEDULED'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    type = db.Column(db.String(20), nullable=False, index=True)
    message = db.Column(db.Text, nullable=False)
    read = db.Column(db.Boolean, default=False, nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    
    def __repr__(self):
        return f'<Notification {self.type} for user {self.user_id}>'
    
    def mark_as_read(self):
        """Mark notification as read"""
        self.read = True
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'type': self.type,
            'message': self.message,
            'read': self.read,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
