"""
Inventory model
"""
from datetime import datetime, date
from app import db
from sqlalchemy import UniqueConstraint


class Inventory(db.Model):
    """Inventory item model"""
    __tablename__ = 'inventory'
    __table_args__ = (
        UniqueConstraint('item_name', 'supplier_id', 'expiration_date', 
                        name='unique_item_supplier_expiry'),
    )
    
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(100), nullable=False, index=True)
    quantity = db.Column(db.Integer, nullable=False, default=0)
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'), nullable=True)
    date_added = db.Column(db.Date, nullable=False, default=date.today)
    expiration_date = db.Column(db.Date, nullable=True, index=True)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f'<Inventory {self.item_name} x{self.quantity}>'
    
    def is_expiring_soon(self, days=3):
        """Check if item is expiring within specified days"""
        if not self.expiration_date:
            return False
        days_until_expiry = (self.expiration_date - date.today()).days
        return 0 <= days_until_expiry <= days
    
    def is_expired(self):
        """Check if item has expired"""
        if not self.expiration_date:
            return False
        return self.expiration_date < date.today()
    
    def is_low_stock(self, threshold_days=3):
        """Check if item is low stock (will run out in threshold_days)"""
        # Simple heuristic: if quantity is very low, consider it low stock
        # In a real system, this would consider usage patterns
        return self.quantity <= 5  # Simplified: 5 or fewer items
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'item_name': self.item_name,
            'quantity': self.quantity,
            'supplier_id': self.supplier_id,
            'supplier_name': self.supplier.name if self.supplier else None,
            'date_added': self.date_added.isoformat() if self.date_added else None,
            'expiration_date': self.expiration_date.isoformat() if self.expiration_date else None,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'is_expiring_soon': self.is_expiring_soon(),
            'is_expired': self.is_expired(),
            'is_low_stock': self.is_low_stock()
        }
