"""
Script to add suppliers to existing database without dropping data
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models.supplier import Supplier


def add_suppliers():
    """Add suppliers to existing database"""
    app = create_app('development')
    
    with app.app_context():
        # Define suppliers to add
        suppliers_to_add = [
            {'name': 'Fresh Foods Co.', 'contact_info': 'contact@freshfoods.com'},
            {'name': 'Quality Meats Ltd.', 'contact_info': 'orders@qualitymeats.com'},
            {'name': 'Garden Vegetables Inc.', 'contact_info': 'sales@gardenveg.com'},
            {'name': 'Dairy Products LLC', 'contact_info': 'info@dairyproducts.com'},
            {'name': 'Ocean Fresh Seafood', 'contact_info': 'orders@oceanfresh.com'},
            {'name': 'Golden Grain Suppliers', 'contact_info': 'sales@goldengrain.com'},
            {'name': 'Spice World Imports', 'contact_info': 'info@spiceworld.com'},
            {'name': 'Premium Poultry Farm', 'contact_info': 'contact@premiumpoultry.com'},
            {'name': 'Organic Produce Market', 'contact_info': 'orders@organicproduce.com'},
            {'name': 'Bakery Essentials Supply', 'contact_info': 'sales@bakeryessentials.com'},
            {'name': 'Fine Wines & Spirits', 'contact_info': 'info@finewines.com'},
            {'name': 'Gourmet Oils & Sauces', 'contact_info': 'contact@gourmetoils.com'},
            {'name': 'Local Farm Fresh', 'contact_info': 'orders@localfarmfresh.com'},
            {'name': 'International Foods Distributor', 'contact_info': 'sales@intlfoodsdist.com'},
            {'name': 'Frozen Foods Depot', 'contact_info': 'orders@frozendepot.com'},
        ]
        
        added_count = 0
        skipped_count = 0
        
        for supplier_data in suppliers_to_add:
            # Check if supplier already exists
            existing = Supplier.query.filter_by(name=supplier_data['name']).first()
            if existing:
                print(f"  ⏭️  Skipped '{supplier_data['name']}' (already exists)")
                skipped_count += 1
            else:
                supplier = Supplier(
                    name=supplier_data['name'],
                    contact_info=supplier_data['contact_info']
                )
                db.session.add(supplier)
                print(f"  ✓  Added '{supplier_data['name']}'")
                added_count += 1
        
        db.session.commit()
        
        print(f"\n{'='*60}")
        print(f"Suppliers added: {added_count}")
        print(f"Suppliers skipped: {skipped_count}")
        print(f"Total suppliers in database: {Supplier.query.count()}")
        print(f"{'='*60}")


if __name__ == '__main__':
    add_suppliers()
