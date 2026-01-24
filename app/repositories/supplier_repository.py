"""
Supplier repository - Data access for suppliers
"""
from app import db
from app.models.supplier import Supplier


class SupplierRepository:
    """Repository for supplier data access"""
    
    @staticmethod
    def get_by_id(supplier_id):
        """Get supplier by ID"""
        return Supplier.query.get(supplier_id)
    
    @staticmethod
    def get_all():
        """Get all suppliers"""
        return Supplier.query.order_by(Supplier.name).all()
    
    @staticmethod
    def get_by_name(name):
        """Get supplier by name"""
        return Supplier.query.filter_by(name=name).first()
    
    @staticmethod
    def create(name, contact_info=None):
        """Create new supplier"""
        supplier = Supplier(name=name, contact_info=contact_info)
        db.session.add(supplier)
        db.session.commit()
        return supplier
    
    @staticmethod
    def update(supplier):
        """Update supplier"""
        db.session.commit()
        return supplier
    
    @staticmethod
    def delete(supplier):
        """Delete supplier"""
        db.session.delete(supplier)
        db.session.commit()
