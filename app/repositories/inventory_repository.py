"""
Inventory repository - Data access for inventory
"""
from app import db
from app.models.inventory import Inventory
from datetime import date, timedelta
from sqlalchemy import and_


class InventoryRepository:
    """Repository for inventory data access"""
    
    @staticmethod
    def get_by_id(item_id):
        """Get inventory item by ID"""
        return Inventory.query.get(item_id)
    
    @staticmethod
    def get_all():
        """Get all inventory items"""
        return Inventory.query.order_by(Inventory.item_name).all()
    
    @staticmethod
    def get_by_name(item_name):
        """Get inventory items by name"""
        return Inventory.query.filter_by(item_name=item_name).all()
    
    @staticmethod
    def get_expiring_soon(days=3):
        """Get items expiring within specified days"""
        expiry_date = date.today() + timedelta(days=days)
        return Inventory.query.filter(
            and_(
                Inventory.expiration_date.isnot(None),
                Inventory.expiration_date >= date.today(),
                Inventory.expiration_date <= expiry_date
            )
        ).all()
    
    @staticmethod
    def get_expired():
        """Get expired items"""
        return Inventory.query.filter(
            Inventory.expiration_date < date.today()
        ).all()
    
    @staticmethod
    def get_low_stock():
        """Get low stock items (quantity <= 5)"""
        return Inventory.query.filter(Inventory.quantity <= 5).all()
    
    @staticmethod
    def find_duplicate(item_name, supplier_id, expiration_date):
        """Find duplicate item (same name, supplier, expiration)"""
        return Inventory.query.filter_by(
            item_name=item_name,
            supplier_id=supplier_id,
            expiration_date=expiration_date
        ).first()
    
    @staticmethod
    def create(item_name, quantity, supplier_id, date_added, expiration_date, created_by):
        """Create new inventory item"""
        item = Inventory(
            item_name=item_name,
            quantity=quantity,
            supplier_id=supplier_id,
            date_added=date_added,
            expiration_date=expiration_date,
            created_by=created_by
        )
        db.session.add(item)
        db.session.commit()
        return item
    
    @staticmethod
    def update(item):
        """Update inventory item"""
        db.session.commit()
        return item
    
    @staticmethod
    def delete(item):
        """Delete inventory item"""
        db.session.delete(item)
        db.session.commit()
    
    @staticmethod
    def update_quantity(item, new_quantity):
        """Update item quantity"""
        item.quantity = new_quantity
        db.session.commit()
        return item
    
    @staticmethod
    def add_quantity(item, amount):
        """Add to item quantity"""
        item.quantity += amount
        db.session.commit()
        return item
    
    @staticmethod
    def remove_quantity(item, amount):
        """Remove from item quantity"""
        if item.quantity >= amount:
            item.quantity -= amount
            db.session.commit()
            return item
        raise ValueError("Insufficient quantity")
