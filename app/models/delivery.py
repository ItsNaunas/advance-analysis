"""
Delivery model
"""
from datetime import datetime, date
from app import db
import json


class Delivery(db.Model):
    """Delivery model"""
    __tablename__ = 'deliveries'
    
    # Status constants
    STATUS_SCHEDULED = 'SCHEDULED'
    STATUS_IN_PROGRESS = 'IN_PROGRESS'
    STATUS_COMPLETED = 'COMPLETED'
    STATUS_CANCELLED = 'CANCELLED'
    
    id = db.Column(db.Integer, primary_key=True)
    delivery_person_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    scheduled_date = db.Column(db.Date, nullable=True, index=True)
    status = db.Column(db.String(20), nullable=False, default=STATUS_SCHEDULED, index=True)
    items_json = db.Column(db.Text, nullable=True)  # JSON array of items
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    completed_at = db.Column(db.DateTime, nullable=True)
    
    def __repr__(self):
        return f'<Delivery {self.id} - {self.status}>'
    
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
        self.items_json = json.dumps(value) if value else None
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'delivery_person_id': self.delivery_person_id,
            'delivery_person_name': self.delivery_person.username if self.delivery_person else None,
            'scheduled_date': self.scheduled_date.isoformat() if self.scheduled_date else None,
            'status': self.status,
            'items': self.items,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None
        }
