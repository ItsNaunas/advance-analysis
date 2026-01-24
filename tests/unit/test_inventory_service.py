"""
Unit tests for inventory service
"""
import pytest
from app.services.inventory_service import InventoryService
from datetime import date, timedelta


def test_add_item_success(app, sample_user, sample_supplier):
    """Test successful item addition"""
    with app.app_context():
        inventory_service = InventoryService()
        item, error = inventory_service.add_item(
            item_name='New Item',
            quantity=5,
            supplier_id=sample_supplier.id,
            date_added=date.today(),
            expiration_date=date.today() + timedelta(days=7),
            user_id=sample_user.id
        )
        
        assert item is not None
        assert error is None
        assert item.item_name == 'New Item'
        assert item.quantity == 5


def test_add_item_duplicate(app, sample_inventory_item, sample_user, sample_supplier):
    """Test adding duplicate item (should merge quantities)"""
    with app.app_context():
        inventory_service = InventoryService()
        original_quantity = sample_inventory_item.quantity
        
        item, error = inventory_service.add_item(
            item_name='Test Item',
            quantity=5,
            supplier_id=sample_supplier.id,
            date_added=date.today(),
            expiration_date=date.today() + timedelta(days=5),
            user_id=sample_user.id
        )
        
        assert item is not None
        assert error is None
        assert item.id == sample_inventory_item.id
        assert item.quantity == original_quantity + 5


def test_remove_item_success(app, sample_inventory_item, sample_user):
    """Test successful item removal"""
    with app.app_context():
        inventory_service = InventoryService()
        original_quantity = sample_inventory_item.quantity
        
        item, error = inventory_service.remove_item(
            sample_inventory_item.id, 3, sample_user.id
        )
        
        assert item is not None
        assert error is None
        assert item.quantity == original_quantity - 3


def test_remove_item_insufficient_quantity(app, sample_inventory_item, sample_user):
    """Test removing more quantity than available"""
    with app.app_context():
        inventory_service = InventoryService()
        
        item, error = inventory_service.remove_item(
            sample_inventory_item.id, 1000, sample_user.id
        )
        
        assert item is None
        assert error is not None


def test_get_expiring_soon(app, sample_inventory_item):
    """Test getting items expiring soon"""
    with app.app_context():
        inventory_service = InventoryService()
        expiring = inventory_service.get_expiring_soon(3)
        
        assert isinstance(expiring, list)
        # sample_inventory_item expires in 5 days, so should not be in 3-day list
        assert len(expiring) == 0 or sample_inventory_item not in expiring
