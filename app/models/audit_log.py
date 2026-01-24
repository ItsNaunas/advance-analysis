"""
Audit log model
"""
from datetime import datetime
from app import db
import json


class AuditLog(db.Model):
    """Audit log model for tracking all system actions"""
    __tablename__ = 'audit_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True, index=True)
    action = db.Column(db.String(50), nullable=False, index=True)
    entity_type = db.Column(db.String(50), nullable=False, index=True)
    entity_id = db.Column(db.Integer, nullable=True, index=True)
    details = db.Column(db.Text, nullable=True)  # JSON with additional details
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    
    def __repr__(self):
        return f'<AuditLog {self.action} by user {self.user_id}>'
    
    @property
    def details_dict(self):
        """Get details as dictionary"""
        if self.details:
            try:
                return json.loads(self.details)
            except json.JSONDecodeError:
                return {}
        return {}
    
    @details_dict.setter
    def details_dict(self, value):
        """Set details from dictionary"""
        self.details = json.dumps(value) if value else None
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'user_name': self.user.username if self.user else None,
            'action': self.action,
            'entity_type': self.entity_type,
            'entity_id': self.entity_id,
            'details': self.details_dict,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None
        }
    
    @staticmethod
    def log_action(user_id, action, entity_type, entity_id=None, details=None):
        """Static method to create audit log entry"""
        log = AuditLog(
            user_id=user_id,
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            details=json.dumps(details) if details else None
        )
        db.session.add(log)
        db.session.commit()
        return log
