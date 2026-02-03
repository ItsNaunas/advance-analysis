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
def sample_chef(app):
    """Create sample chef for testing"""
    with app.app_context():
        user = User(
            username='chef',
            email='chef@example.com',
            password_hash=hash_password('password123'),
            role=User.ROLE_CHEF
        )
        db.session.add(user)
        db.session.commit()
        user_id = user.id
        username = user.username
        
    # Return a simple object with the data we need
    class UserData:
        def __init__(self, id, username):
            self.id = id
            self.username = username
            
    return UserData(user_id, username)


@pytest.fixture
def sample_delivery_person(app):
    """Create sample delivery person for testing"""
    with app.app_context():
        user = User(
            username='delivery1',
            email='delivery@example.com',
            password_hash=hash_password('password123'),
            role=User.ROLE_DELIVERY_PERSON
        )
        db.session.add(user)
        db.session.commit()
        user_id = user.id
        username = user.username
        
    # Return a simple object with the data we need
    class UserData:
        def __init__(self, id, username):
            self.id = id
            self.username = username
            
    return UserData(user_id, username)


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
