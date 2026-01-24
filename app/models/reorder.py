"""
Reorder model
"""
from datetime import datetime, date
from app import db
import json


class Reorder(db.Model):
    """Reorder model"""
    __tablename__ = 'reorders'
    
    # Status constants
    STATUS_PENDING = 'PENDING'
    STATUS_CONFIRMED = 'CONFIRMED'
    STATUS_CANCELLED = 'CANCELLED'
    STATUS_SENT = 'SENT'
    
    id = db.Column(db.Integer, primary_key=True)
    generated_date = db.Column(db.Date, nullable=False, default=date.today, index=True)
    status = db.Column(db.String(20), nullable=False, default=STATUS_PENDING, index=True)
    items_json = db.Column(db.Text, nullable=False)  # JSON array of items with quantities
    confirmed_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    confirmed_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f'<Reorder {self.id} - {self.status}>'
    
    @property
    def items(self):
        """Get items as list"""
        if self.items_json:
            try:
                return json.loads(self.items_json)
            except json.JSONDecodeError:
                return []
        return []
    
    @items.setter
    def items(self, value):
        """Set items from list"""
        self.items_json = json.dumps(value) if value else '[]'
    
    def confirm(self, user_id):
        """Confirm reorder"""
        self.status = self.STATUS_CONFIRMED
        self.confirmed_by = user_id
        self.confirmed_at = datetime.utcnow()
    
    def cancel(self):
        """Cancel reorder"""
        self.status = self.STATUS_CANCELLED
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'generated_date': self.generated_date.isoformat() if self.generated_date else None,
            'status': self.status,
            'items': self.items,
            'confirmed_by': self.confirmed_by,
            'confirmed_by_name': self.confirmed_by_user.username if self.confirmed_by_user else None,
            'confirmed_at': self.confirmed_at.isoformat() if self.confirmed_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
