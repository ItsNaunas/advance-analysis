"""
Inventory service - Business logic for inventory management
"""
from app.repositories.inventory_repository import InventoryRepository
from app.repositories.audit_repository import AuditRepository
from app.models.audit_log import AuditLog
from datetime import date
from app import db


class InventoryService:
    """Service for inventory operations"""
    
    def __init__(self):
        self.inventory_repo = InventoryRepository()
        self.audit_repo = AuditRepository()
    
    def add_item(self, item_name, quantity, supplier_id, date_added, expiration_date, user_id):
        """Add new inventory item"""
        # Check for duplicate
        duplicate = self.inventory_repo.find_duplicate(item_name, supplier_id, expiration_date)
        if duplicate:
            # If duplicate exists, add to quantity instead
            self.inventory_repo.add_quantity(duplicate, quantity)
            AuditLog.log_action(
                user_id, 'INVENTORY_QUANTITY_ADDED', 'INVENTORY', duplicate.id,
                {'item_name': item_name, 'quantity_added': quantity}
            )
            return duplicate, None
        
        # Create new item
        item = self.inventory_repo.create(
            item_name=item_name,
            quantity=quantity,
            supplier_id=supplier_id,
            date_added=date_added or date.today(),
            expiration_date=expiration_date,
            created_by=user_id
        )
        
        AuditLog.log_action(
            user_id, 'INVENTORY_ITEM_ADDED', 'INVENTORY', item.id,
            {'item_name': item_name, 'quantity': quantity}
        )
        
        return item, None
    
    def remove_item(self, item_id, quantity, user_id):
        """Remove quantity from inventory item"""
        item = self.inventory_repo.get_by_id(item_id)
        
        if not item:
            return None, "Item not found"
        
        try:
            self.inventory_repo.remove_quantity(item, quantity)
            AuditLog.log_action(
                user_id, 'INVENTORY_ITEM_REMOVED', 'INVENTORY', item.id,
                {'item_name': item.item_name, 'quantity_removed': quantity}
            )
            return item, None
        except ValueError as e:
            return None, str(e)
    
    def update_item(self, item_id, item_name=None, quantity=None, expiration_date=None, user_id=None):
        """Update inventory item"""
        item = self.inventory_repo.get_by_id(item_id)
        
        if not item:
            return None, "Item not found"
        
        changes = {}
        if item_name is not None:
            changes['item_name'] = item.item_name
            item.item_name = item_name
        if quantity is not None:
            changes['quantity'] = item.quantity
            item.quantity = quantity
        if expiration_date is not None:
            changes['expiration_date'] = item.expiration_date
            item.expiration_date = expiration_date
        
        self.inventory_repo.update(item)
        
        if user_id:
            AuditLog.log_action(
                user_id, 'INVENTORY_ITEM_UPDATED', 'INVENTORY', item.id,
                {'changes': changes}
            )
        
        return item, None
    
    def delete_item(self, item_id, user_id):
        """Delete inventory item"""
        item = self.inventory_repo.get_by_id(item_id)
        
        if not item:
            return None, "Item not found"
        
        item_name = item.item_name
        self.inventory_repo.delete(item)
        
        AuditLog.log_action(
            user_id, 'INVENTORY_ITEM_DELETED', 'INVENTORY', item_id,
            {'item_name': item_name}
        )
        
        return True, None
    
    def get_all_items(self):
        """Get all inventory items"""
        return self.inventory_repo.get_all()
    
    def get_item(self, item_id):
        """Get inventory item by ID"""
        return self.inventory_repo.get_by_id(item_id)
    
    def get_expiring_soon(self, days=3):
        """Get items expiring soon"""
        return self.inventory_repo.get_expiring_soon(days)
    
    def get_low_stock(self):
        """Get low stock items"""
        return self.inventory_repo.get_low_stock()
    
    def get_expired(self):
        """Get expired items"""
        return self.inventory_repo.get_expired()
