"""
Reorder service - Business logic for automated reordering
"""
from app import db
from app.models.reorder import Reorder
from app.models.user import User
from app.services.inventory_service import InventoryService
from app.services.notification_service import NotificationService
from app.models.audit_log import AuditLog
from datetime import date, datetime
from flask import current_app
import json


class ReorderService:
    """Service for reorder operations"""
    
    def __init__(self):
        self.inventory_service = InventoryService()
    
    def generate_reorder_list(self):
        """Generate reorder list based on low stock and expiring items"""
        # Get low stock items
        low_stock_items = self.inventory_service.get_low_stock()
        
        # Get items expiring soon (within 3 days)
        expiring_items = self.inventory_service.get_expiring_soon(3)
        
        # Combine and deduplicate items
        items_to_reorder = {}
        
        for item in low_stock_items:
            key = (item.item_name, item.supplier_id)
            if key not in items_to_reorder:
                items_to_reorder[key] = {
                    'item_name': item.item_name,
                    'supplier_id': item.supplier_id,
                    'supplier_name': item.supplier.name if item.supplier else None,
                    'current_quantity': item.quantity,
                    'suggested_quantity': max(20 - item.quantity, 10)  # Simple heuristic
                }
        
        for item in expiring_items:
            key = (item.item_name, item.supplier_id)
            if key not in items_to_reorder:
                items_to_reorder[key] = {
                    'item_name': item.item_name,
                    'supplier_id': item.supplier_id,
                    'supplier_name': item.supplier.name if item.supplier else None,
                    'current_quantity': item.quantity,
                    'suggested_quantity': max(20 - item.quantity, 10)
                }
        
        # Create reorder
        reorder = Reorder(
            generated_date=date.today(),
            status=Reorder.STATUS_PENDING,
            items_json=json.dumps(list(items_to_reorder.values()))
        )
        db.session.add(reorder)
        db.session.commit()
        
        # Create notification for Head Chefs
        head_chefs = User.query.filter_by(role=User.ROLE_HEAD_CHEF).all()
        from app.models.notification import Notification
        from app.services.notification_service import NotificationService
        notif_service = NotificationService()
        
        for chef in head_chefs:
            notif_service.create_notification(
                chef.id,
                Notification.TYPE_REORDER_READY,
                f"New reorder list generated with {len(items_to_reorder)} items. Please review and confirm."
            )
        
        AuditLog.log_action(None, 'REORDER_GENERATED', 'REORDER', reorder.id, {
            'item_count': len(items_to_reorder)
        })
        
        return reorder
    
    def get_all_reorders(self):
        """Get all reorders"""
        return Reorder.query.order_by(Reorder.generated_date.desc()).all()
    
    def get_reorder(self, reorder_id):
        """Get reorder by ID"""
        return Reorder.query.get(reorder_id)
    
    def get_pending_reorders(self):
        """Get pending reorders"""
        return Reorder.query.filter_by(status=Reorder.STATUS_PENDING).all()
    
    def confirm_reorder(self, reorder_id, user_id):
        """Confirm reorder (Head Chef only)"""
        reorder = self.get_reorder(reorder_id)
        
        if not reorder:
            return None, "Reorder not found"
        
        if reorder.status != Reorder.STATUS_PENDING:
            return None, "Reorder is not in pending status"
        
        reorder.confirm(user_id)
        db.session.commit()
        
        AuditLog.log_action(user_id, 'REORDER_CONFIRMED', 'REORDER', reorder_id, {})
        
        return reorder, None
    
    def cancel_reorder(self, reorder_id, user_id):
        """Cancel reorder (Head Chef only)"""
        reorder = self.get_reorder(reorder_id)
        
        if not reorder:
            return None, "Reorder not found"
        
        if reorder.status != Reorder.STATUS_PENDING:
            return None, "Only pending reorders can be cancelled"
        
        reorder.cancel()
        db.session.commit()
        
        AuditLog.log_action(user_id, 'REORDER_CANCELLED', 'REORDER', reorder_id, {})
        
        return reorder, None
