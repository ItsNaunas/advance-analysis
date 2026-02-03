"""
Script to verify suppliers in the database
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models.supplier import Supplier


def verify_suppliers():
    """Verify suppliers in the database"""
    app = create_app('development')
    
    with app.app_context():
        suppliers = Supplier.query.order_by(Supplier.name).all()
        
        print(f"\n{'='*60}")
        print(f"Total Suppliers in Database: {len(suppliers)}")
        print(f"{'='*60}\n")
        
        if suppliers:
            for idx, supplier in enumerate(suppliers, 1):
                print(f"{idx:2d}. {supplier.name}")
                print(f"    Contact: {supplier.contact_info}")
                print()
        else:
            print("⚠️  No suppliers found in database!")
        
        print(f"{'='*60}")


if __name__ == '__main__':
    verify_suppliers()
