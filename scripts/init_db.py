"""
Script to initialize database with sample data
"""
import sys
import os
from datetime import date, timedelta

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models.user import User
from app.models.supplier import Supplier
from app.models.inventory import Inventory
from app.utils.password_hasher import hash_password

def init_database():
    """Initialize database with sample data"""
    app = create_app('development')
    
    with app.app_context():
        # Drop all tables and recreate
        db.drop_all()
        db.create_all()
        
        # Create users
        users = [
            User(username='admin', email='admin@ffsmart.com', 
                 password_hash=hash_password('password'), role=User.ROLE_ADMIN),
            User(username='headchef', email='headchef@ffsmart.com', 
                 password_hash=hash_password('password'), role=User.ROLE_HEAD_CHEF),
            User(username='chef1', email='chef1@ffsmart.com', 
                 password_hash=hash_password('password'), role=User.ROLE_CHEF),
            User(username='chef2', email='chef2@ffsmart.com', 
                 password_hash=hash_password('password'), role=User.ROLE_CHEF),
            User(username='delivery1', email='delivery1@ffsmart.com', 
                 password_hash=hash_password('password'), role=User.ROLE_DELIVERY_PERSON),
            User(username='healthsafety', email='healthsafety@ffsmart.com', 
                 password_hash=hash_password('password'), role=User.ROLE_HEALTH_SAFETY_OFFICER),
        ]
        
        for user in users:
            db.session.add(user)
        db.session.commit()
        
        # Create suppliers
        suppliers = [
            Supplier(name='Fresh Foods Co.', contact_info='contact@freshfoods.com'),
            Supplier(name='Quality Meats Ltd.', contact_info='orders@qualitymeats.com'),
            Supplier(name='Garden Vegetables Inc.', contact_info='sales@gardenveg.com'),
            Supplier(name='Dairy Products LLC', contact_info='info@dairyproducts.com'),
            Supplier(name='Ocean Fresh Seafood', contact_info='orders@oceanfresh.com'),
            Supplier(name='Golden Grain Suppliers', contact_info='sales@goldengrain.com'),
            Supplier(name='Spice World Imports', contact_info='info@spiceworld.com'),
            Supplier(name='Premium Poultry Farm', contact_info='contact@premiumpoultry.com'),
            Supplier(name='Organic Produce Market', contact_info='orders@organicproduce.com'),
            Supplier(name='Bakery Essentials Supply', contact_info='sales@bakeryessentials.com'),
            Supplier(name='Fine Wines & Spirits', contact_info='info@finewines.com'),
            Supplier(name='Gourmet Oils & Sauces', contact_info='contact@gourmetoils.com'),
            Supplier(name='Local Farm Fresh', contact_info='orders@localfarmfresh.com'),
            Supplier(name='International Foods Distributor', contact_info='sales@intlfoodsdist.com'),
            Supplier(name='Frozen Foods Depot', contact_info='orders@frozendepot.com'),
        ]
        
        for supplier in suppliers:
            db.session.add(supplier)
        db.session.commit()
        
        # Create sample inventory items
        head_chef = User.query.filter_by(username='headchef').first()
        chef1 = User.query.filter_by(username='chef1').first()
        
        inventory_items = [
            Inventory(item_name='Chicken Breast', quantity=25, supplier_id=2, 
                     date_added=date.today() - timedelta(days=2), 
                     expiration_date=date.today() + timedelta(days=2), created_by=head_chef.id),
            Inventory(item_name='Ground Beef', quantity=15, supplier_id=2, 
                     date_added=date.today() - timedelta(days=1), 
                     expiration_date=date.today() + timedelta(days=1), created_by=head_chef.id),
            Inventory(item_name='Lettuce', quantity=8, supplier_id=3, 
                     date_added=date.today() - timedelta(days=3), 
                     expiration_date=date.today() + timedelta(days=1), created_by=chef1.id),
            Inventory(item_name='Tomatoes', quantity=12, supplier_id=3, 
                     date_added=date.today() - timedelta(days=2), 
                     expiration_date=date.today() + timedelta(days=3), created_by=chef1.id),
            Inventory(item_name='Milk', quantity=4, supplier_id=4, 
                     date_added=date.today() - timedelta(days=1), 
                     expiration_date=date.today() + timedelta(days=2), created_by=head_chef.id),
            Inventory(item_name='Cheese', quantity=6, supplier_id=4, 
                     date_added=date.today() - timedelta(days=5), 
                     expiration_date=date.today() - timedelta(days=1), created_by=head_chef.id),  # Expired
            Inventory(item_name='Onions', quantity=20, supplier_id=3, 
                     date_added=date.today() - timedelta(days=7), 
                     expiration_date=date.today() + timedelta(days=10), created_by=chef1.id),
            Inventory(item_name='Potatoes', quantity=30, supplier_id=3, 
                     date_added=date.today() - timedelta(days=5), 
                     expiration_date=date.today() + timedelta(days=15), created_by=chef1.id),
        ]
        
        for item in inventory_items:
            db.session.add(item)
        db.session.commit()
        
        print("Database initialized successfully!")
        print("\nSample users created:")
        print("  - admin / password (Admin)")
        print("  - headchef / password (Head Chef)")
        print("  - chef1 / password (Chef)")
        print("  - chef2 / password (Chef)")
        print("  - delivery1 / password (Delivery Person)")
        print("  - healthsafety / password (Health & Safety Officer)")

if __name__ == '__main__':
    init_database()
