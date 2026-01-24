"""
Pytest configuration and fixtures
"""
import pytest
from app import create_app, db
from app.models.user import User
from app.models.supplier import Supplier
from app.models.inventory import Inventory
from app.utils.password_hasher import hash_password
from datetime import date, timedelta


@pytest.fixture
def app():
    """Create application for testing"""
    app = create_app('testing')
    
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()


@pytest.fixture
def runner(app):
    """Create test CLI runner"""
    return app.test_cli_runner()


@pytest.fixture
def sample_user(app):
    """Create sample user for testing"""
    with app.app_context():
        user = User(
            username='testuser',
            email='test@example.com',
            password_hash=hash_password('password'),
            role=User.ROLE_CHEF
        )
        db.session.add(user)
        db.session.commit()
        return user


@pytest.fixture
def sample_head_chef(app):
    """Create sample head chef for testing"""
    with app.app_context():
        user = User(
            username='headchef',
            email='headchef@example.com',
            password_hash=hash_password('password'),
            role=User.ROLE_HEAD_CHEF
        )
        db.session.add(user)
        db.session.commit()
        return user


@pytest.fixture
def sample_supplier(app):
    """Create sample supplier for testing"""
    with app.app_context():
        supplier = Supplier(
            name='Test Supplier',
            contact_info='test@supplier.com'
        )
        db.session.add(supplier)
        db.session.commit()
        return supplier


@pytest.fixture
def sample_inventory_item(app, sample_user, sample_supplier):
    """Create sample inventory item for testing"""
    with app.app_context():
        item = Inventory(
            item_name='Test Item',
            quantity=10,
            supplier_id=sample_supplier.id,
            date_added=date.today(),
            expiration_date=date.today() + timedelta(days=5),
            created_by=sample_user.id
        )
        db.session.add(item)
        db.session.commit()
        return item
