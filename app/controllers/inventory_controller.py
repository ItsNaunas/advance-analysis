"""
Inventory controller - Handles inventory management routes
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app.services.inventory_service import InventoryService
from app.repositories.supplier_repository import SupplierRepository
from app.middleware.rbac_middleware import require_authenticated
from datetime import datetime

inventory_bp = Blueprint('inventory', __name__, url_prefix='/inventory')
inventory_service = InventoryService()


@inventory_bp.route('', methods=['GET'])
@login_required
def list():
    """List all inventory items"""
    items = inventory_service.get_all_items()
    return render_template('inventory/list.html', items=items)


@inventory_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    """Add new inventory item"""
    from app.repositories.supplier_repository import SupplierRepository
    supplier_repo = SupplierRepository()
    
    if request.method == 'POST':
        item_name = request.form.get('item_name', '').strip()
        quantity = request.form.get('quantity', '0')
        supplier_id = request.form.get('supplier_id') or None
        date_added = request.form.get('date_added')
        expiration_date = request.form.get('expiration_date') or None
        
        # Validate inputs
        if not item_name:
            flash('Item name is required.', 'error')
            suppliers = supplier_repo.get_all()
            return render_template('inventory/add.html', suppliers=suppliers)
        
        try:
            quantity = int(quantity)
            if quantity < 0:
                raise ValueError
        except ValueError:
            flash('Quantity must be a positive number.', 'error')
            suppliers = supplier_repo.get_all()
            return render_template('inventory/add.html', suppliers=suppliers)
        
        # Parse dates
        date_added_parsed = None
        if date_added:
            try:
                date_added_parsed = datetime.strptime(date_added, '%Y-%m-%d').date()
            except ValueError:
                flash('Invalid date format.', 'error')
                suppliers = supplier_repo.get_all()
                return render_template('inventory/add.html', suppliers=suppliers)
        
        expiration_date_parsed = None
        if expiration_date:
            try:
                expiration_date_parsed = datetime.strptime(expiration_date, '%Y-%m-%d').date()
            except ValueError:
                flash('Invalid expiration date format.', 'error')
                suppliers = supplier_repo.get_all()
                return render_template('inventory/add.html', suppliers=suppliers)
        
        # Add item
        item, error = inventory_service.add_item(
            item_name=item_name,
            quantity=quantity,
            supplier_id=int(supplier_id) if supplier_id else None,
            date_added=date_added_parsed,
            expiration_date=expiration_date_parsed,
            user_id=current_user.id
        )
        
        if item:
            flash(f'Item "{item_name}" added successfully.', 'success')
            return redirect(url_for('inventory.list'))
        else:
            flash(error or 'Failed to add item.', 'error')
    
    suppliers = supplier_repo.get_all()
    return render_template('inventory/add.html', suppliers=suppliers)


@inventory_bp.route('/<int:item_id>/remove', methods=['POST'])
@login_required
def remove(item_id):
    """Remove quantity from inventory item"""
    quantity = request.form.get('quantity', '0')
    
    try:
        quantity = int(quantity)
        if quantity <= 0:
            raise ValueError
    except ValueError:
        flash('Quantity must be a positive number.', 'error')
        return redirect(url_for('inventory.list'))
    
    item, error = inventory_service.remove_item(item_id, quantity, current_user.id)
    
    if item:
        flash(f'Removed {quantity} of "{item.item_name}".', 'success')
    else:
        flash(error or 'Failed to remove item.', 'error')
    
    return redirect(url_for('inventory.list'))


@inventory_bp.route('/api', methods=['GET'])
@login_required
def api_list():
    """API endpoint to get all inventory items as JSON"""
    items = inventory_service.get_all_items()
    return jsonify([item.to_dict() for item in items])


@inventory_bp.route('/api', methods=['POST'])
@login_required
def api_add():
    """API endpoint to add inventory item"""
    data = request.get_json()
    
    item_name = data.get('item_name', '').strip()
    quantity = data.get('quantity', 0)
    supplier_id = data.get('supplier_id')
    date_added = data.get('date_added')
    expiration_date = data.get('expiration_date')
    
    if not item_name:
        return jsonify({'success': False, 'error': 'Item name is required'}), 400
    
    try:
        quantity = int(quantity)
    except (ValueError, TypeError):
        return jsonify({'success': False, 'error': 'Invalid quantity'}), 400
    
    # Parse dates
    from datetime import datetime
    date_added_parsed = None
    if date_added:
        try:
            date_added_parsed = datetime.strptime(date_added, '%Y-%m-%d').date()
        except ValueError:
            pass
    
    expiration_date_parsed = None
    if expiration_date:
        try:
            expiration_date_parsed = datetime.strptime(expiration_date, '%Y-%m-%d').date()
        except ValueError:
            pass
    
    item, error = inventory_service.add_item(
        item_name=item_name,
        quantity=quantity,
        supplier_id=int(supplier_id) if supplier_id else None,
        date_added=date_added_parsed,
        expiration_date=expiration_date_parsed,
        user_id=current_user.id
    )
    
    if item:
        return jsonify({'success': True, 'item': item.to_dict()}), 201
    else:
        return jsonify({'success': False, 'error': error}), 400
