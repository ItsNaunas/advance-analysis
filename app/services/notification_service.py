"""
Notification service - Business logic for notifications
"""
from app import db
from app.models.notification import Notification
from app.models.user import User
from app.services.inventory_service import InventoryService
from datetime import datetime
from flask import current_app


class NotificationService:
    """Service for notification operations"""
    
    def __init__(self):
        self.inventory_service = InventoryService()
    
    def create_notification(self, user_id, notification_type, message):
        """Create a notification"""
        notification = Notification(
            user_id=user_id,
            type=notification_type,
            message=message
        )
        db.session.add(notification)
        db.session.commit()
        return notification
    
    def get_user_notifications(self, user_id, unread_only=False):
        """Get notifications for a user"""
        query = Notification.query.filter_by(user_id=user_id)
        if unread_only:
            query = query.filter_by(read=False)
        return query.order_by(Notification.created_at.desc()).all()
    
    def get_unread_count(self, user_id):
        """Get count of unread notifications"""
        return Notification.query.filter_by(user_id=user_id, read=False).count()
    
    def mark_as_read(self, notification_id, user_id):
        """Mark a notification as read"""
        notification = Notification.query.get(notification_id)
        if notification and notification.user_id == user_id:
            notification.mark_as_read()
            db.session.commit()
            return True
        return False
    
    def mark_all_as_read(self, user_id):
        """Mark all notifications as read for a user"""
        Notification.query.filter_by(user_id=user_id, read=False).update({'read': True})
        db.session.commit()
        return True
    
    def check_and_create_expiry_warnings(self):
        """Check for expiring items and create notifications"""
        days = current_app.config.get('EXPIRY_WARNING_DAYS', 3)
        expiring_items = self.inventory_service.get_expiring_soon(days)
        
        # Get Head Chef users
        head_chefs = User.query.filter_by(role=User.ROLE_HEAD_CHEF).all()
        
        notifications_created = 0
        for item in expiring_items:
            days_until_expiry = (item.expiration_date - datetime.now().date()).days
            message = f"Item '{item.item_name}' is expiring in {days_until_expiry} day(s). " \
                     f"Current quantity: {item.quantity}"
            if item.supplier:
                message += f" Supplier: {item.supplier.name}"
            
            for chef in head_chefs:
                # Check if notification already exists
                existing = Notification.query.filter_by(
                    user_id=chef.id,
                    type=Notification.TYPE_EXPIRY_WARNING,
                    read=False
                ).filter(
                    Notification.message.like(f"%{item.item_name}%")
                ).first()
                
                if not existing:
                    self.create_notification(
                        chef.id,
                        Notification.TYPE_EXPIRY_WARNING,
                        message
                    )
                    notifications_created += 1
        
        return notifications_created
    
    def check_and_create_low_stock_warnings(self):
        """Check for low stock items and create notifications"""
        low_stock_items = self.inventory_service.get_low_stock()
        
        # Get Head Chef users
        head_chefs = User.query.filter_by(role=User.ROLE_HEAD_CHEF).all()
        
        notifications_created = 0
        for item in low_stock_items:
            message = f"Item '{item.item_name}' is running low. " \
                     f"Current quantity: {item.quantity}"
            if item.supplier:
                message += f" Suggested supplier: {item.supplier.name}"
            
            for chef in head_chefs:
                # Check if notification already exists
                existing = Notification.query.filter_by(
                    user_id=chef.id,
                    type=Notification.TYPE_LOW_STOCK,
                    read=False
                ).filter(
                    Notification.message.like(f"%{item.item_name}%")
                ).first()
                
                if not existing:
                    self.create_notification(
                        chef.id,
                        Notification.TYPE_LOW_STOCK,
                        message
                    )
                    notifications_created += 1
        
        return notifications_created
