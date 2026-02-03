"""
Delivery controller - Handles delivery management routes
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app.models.delivery import Delivery
from app.models.user import User
from app.models.audit_log import AuditLog
from app.middleware.rbac_middleware import require_role
from app import db
from datetime import date, datetime
import json

delivery_bp = Blueprint('delivery', __name__, url_prefix='/deliveries')


@delivery_bp.route('', methods=['GET'])
@login_required
@require_role(User.ROLE_DELIVERY_PERSON, User.ROLE_HEAD_CHEF, User.ROLE_ADMIN)
def list():
    """List deliveries for delivery person"""
    if current_user.role == User.ROLE_DELIVERY_PERSON:
        deliveries = Delivery.query.filter_by(delivery_person_id=current_user.id)\
            .order_by(Delivery.scheduled_date.desc()).all()
    else:
        deliveries = Delivery.query.order_by(Delivery.scheduled_date.desc()).all()
    
    return render_template('delivery/dashboard.html', deliveries=deliveries)


@delivery_bp.route('/<int:delivery_id>', methods=['GET'])
@login_required
@require_role(User.ROLE_DELIVERY_PERSON, User.ROLE_HEAD_CHEF, User.ROLE_ADMIN)
def detail(delivery_id):
    """Delivery detail page"""
    delivery = Delivery.query.get_or_404(delivery_id)
    
    # Check access
    if current_user.role == User.ROLE_DELIVERY_PERSON and delivery.delivery_person_id != current_user.id:
        flash('You do not have access to this delivery.', 'error')
        return redirect(url_for('delivery.list'))
    
    return render_template('delivery/detail.html', delivery=delivery)


@delivery_bp.route('/<int:delivery_id>/confirm', methods=['POST'])
@login_required
@require_role(User.ROLE_DELIVERY_PERSON, User.ROLE_HEAD_CHEF, User.ROLE_ADMIN)
def confirm(delivery_id):
    """Confirm delivery"""
    delivery = Delivery.query.get_or_404(delivery_id)
    
    # Check access
    if current_user.role == User.ROLE_DELIVERY_PERSON and delivery.delivery_person_id != current_user.id:
        flash('You do not have access to this delivery.', 'error')
        return redirect(url_for('delivery.list'))
    
    delivery.status = Delivery.STATUS_COMPLETED
    delivery.completed_at = datetime.utcnow()
    db.session.commit()
    
    AuditLog.log_action(
        current_user.id,
        'DELIVERY_CONFIRMED',
        'DELIVERY',
        delivery_id,
        {}
    )
    
    flash('Delivery confirmed successfully.', 'success')
    return redirect(url_for('delivery.list'))


@delivery_bp.route('/request-access', methods=['POST'])
@login_required
@require_role(User.ROLE_DELIVERY_PERSON)
def request_access():
    """Request rear door access (simulated)"""
    # Simulate door access - in real system, this would interface with hardware
    # For now, we just log the request and grant access
    AuditLog.log_action(
        current_user.id,
        'REAR_DOOR_ACCESS_REQUESTED',
        'DELIVERY',
        None,
        {}
    )
    
    return jsonify({
        'success': True,
        'access_granted': True,
        'message': 'Rear door access granted'
    })


@delivery_bp.route('/new', methods=['GET'])
@login_required
@require_role(User.ROLE_DELIVERY_PERSON)
def new():
    """Display form to create new delivery"""
    return render_template('delivery/new_delivery.html')


@delivery_bp.route('/submit', methods=['POST'])
@login_required
@require_role(User.ROLE_DELIVERY_PERSON)
def submit():
    """Submit a new delivery"""
    try:
        # Get items from form
        items_data = request.get_json()
        items = items_data.get('items', [])
        
        if not items:
            return jsonify({
                'success': False,
                'message': 'No items provided'
            }), 400
        
        # Create new delivery with auto-populated fields
        delivery = Delivery(
            delivery_person_id=current_user.id,  # Auto-add delivery person
            scheduled_date=date.today(),          # Auto-add date
            status=Delivery.STATUS_SCHEDULED,
            items=items
        )
        
        db.session.add(delivery)
        db.session.commit()
        
        # Log the action
        AuditLog.log_action(
            current_user.id,
            'DELIVERY_SUBMITTED',
            'DELIVERY',
            delivery.id,
            {'items_count': len(items)}
        )
        
        return jsonify({
            'success': True,
            'message': 'Delivery submitted successfully',
            'delivery_id': delivery.id,  # Auto-generated delivery ID
            'delivery_person': current_user.username,
            'date': delivery.created_at.isoformat()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error submitting delivery: {str(e)}'
        }), 500


@delivery_bp.route('/api', methods=['GET'])
@login_required
@require_role(User.ROLE_DELIVERY_PERSON, User.ROLE_HEAD_CHEF, User.ROLE_ADMIN)
def api_list():
    """API endpoint to get deliveries as JSON"""
    if current_user.role == User.ROLE_DELIVERY_PERSON:
        deliveries = Delivery.query.filter_by(delivery_person_id=current_user.id).all()
    else:
        deliveries = Delivery.query.all()
    
    return jsonify([delivery.to_dict() for delivery in deliveries])
