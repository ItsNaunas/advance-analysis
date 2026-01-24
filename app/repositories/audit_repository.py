"""
Audit log repository - Data access for audit logs
"""
from app import db
from app.models.audit_log import AuditLog
from datetime import datetime, timedelta
from sqlalchemy import desc


class AuditRepository:
    """Repository for audit log data access"""
    
    @staticmethod
    def get_by_id(log_id):
        """Get audit log by ID"""
        return AuditLog.query.get(log_id)
    
    @staticmethod
    def get_all(limit=100, offset=0):
        """Get all audit logs with pagination"""
        return AuditLog.query.order_by(desc(AuditLog.timestamp)).limit(limit).offset(offset).all()
    
    @staticmethod
    def get_by_user(user_id, limit=100):
        """Get audit logs for specific user"""
        return AuditLog.query.filter_by(user_id=user_id)\
            .order_by(desc(AuditLog.timestamp)).limit(limit).all()
    
    @staticmethod
    def get_by_action(action, limit=100):
        """Get audit logs by action type"""
        return AuditLog.query.filter_by(action=action)\
            .order_by(desc(AuditLog.timestamp)).limit(limit).all()
    
    @staticmethod
    def get_by_entity(entity_type, entity_id):
        """Get audit logs for specific entity"""
        return AuditLog.query.filter_by(
            entity_type=entity_type,
            entity_id=entity_id
        ).order_by(desc(AuditLog.timestamp)).all()
    
    @staticmethod
    def get_recent(days=7):
        """Get recent audit logs"""
        since = datetime.utcnow() - timedelta(days=days)
        return AuditLog.query.filter(AuditLog.timestamp >= since)\
            .order_by(desc(AuditLog.timestamp)).all()
    
    @staticmethod
    def create(user_id, action, entity_type, entity_id=None, details=None):
        """Create audit log entry"""
        return AuditLog.log_action(user_id, action, entity_type, entity_id, details)
    
    @staticmethod
    def count():
        """Get total count of audit logs"""
        return AuditLog.query.count()
