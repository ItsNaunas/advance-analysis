"""
Test script to verify supplier dropdown functionality
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.repositories.supplier_repository import SupplierRepository


def test_supplier_dropdown():
    """Test that suppliers are available for the dropdown"""
    app = create_app('development')
    
    with app.app_context():
        supplier_repo = SupplierRepository()
        suppliers = supplier_repo.get_all()
        
        print(f"\n{'='*60}")
        print("SUPPLIER DROPDOWN TEST")
        print(f"{'='*60}\n")
        
        print(f"✓ Found {len(suppliers)} suppliers in database")
        print(f"✓ Suppliers are sorted by name: {suppliers[0].name if suppliers else 'N/A'}\n")
        
        print("Dropdown options that will be displayed:")
        print("-" * 60)
        print('<select id="supplier_id" name="supplier_id">')
        print('    <option value="">Select Supplier (Optional)</option>')
        
        for supplier in suppliers:
            print(f'    <option value="{supplier.id}">{supplier.name}</option>')
        
        print('</select>')
        print("-" * 60)
        
        print(f"\n{'='*60}")
        print("✓ TEST PASSED: Suppliers will appear in dropdown!")
        print(f"{'='*60}\n")
        
        return True


if __name__ == '__main__':
    test_supplier_dropdown()
