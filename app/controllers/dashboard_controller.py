"""
Dashboard controller - Handles role-specific dashboards
"""
from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from app.models.user import User
from app.services.inventory_service import InventoryService
from app.services.reorder_service import ReorderService
from app.services.notification_service import NotificationService

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')
inventory_service = InventoryService()
reorder_service = ReorderService()
notification_service = NotificationService()


@dashboard_bp.route('', methods=['GET'])
@dashboard_bp.route('/', methods=['GET'])
@login_required
def index():
    """Route to appropriate dashboard based on user role"""
    if current_user.role == User.ROLE_HEAD_CHEF:
        return redirect(url_for('dashboard.head_chef'))
    elif current_user.role == User.ROLE_CHEF:
        return redirect(url_for('dashboard.chef'))
    elif current_user.role == User.ROLE_DELIVERY_PERSON:
        return redirect(url_for('dashboard.delivery_person'))
    elif current_user.role == User.ROLE_ADMIN:
        return redirect(url_for('dashboard.admin'))
    elif current_user.role == User.ROLE_HEALTH_SAFETY_OFFICER:
        return redirect(url_for('dashboard.health_safety'))
    else:
        return redirect(url_for('inventory.list'))


@dashboard_bp.route('/head-chef', methods=['GET'])
@login_required
def head_chef():
    """Head Chef dashboard"""
    if current_user.role != User.ROLE_HEAD_CHEF:
        from flask import abort
        abort(403)
    
    # Get dashboard data
    all_items = inventory_service.get_all_items()
    expiring_items = inventory_service.get_expiring_soon(3)
    low_stock_items = inventory_service.get_low_stock()
    pending_reorders = reorder_service.get_pending_reorders()
    unread_count = notification_service.get_unread_count(current_user.id)
    
    return render_template(
        'dashboards/head_chef.html',
        all_items=all_items,
        expiring_items=expiring_items,
        low_stock_items=low_stock_items,
        pending_reorders=pending_reorders,
        unread_count=unread_count
    )


@dashboard_bp.route('/chef', methods=['GET'])
@login_required
def chef():
    """Chef dashboard"""
    if current_user.role != User.ROLE_CHEF:
        from flask import abort
        abort(403)
    
    # Get inventory for chef
    all_items = inventory_service.get_all_items()
    
    return render_template('dashboards/chef.html', items=all_items)


@dashboard_bp.route('/delivery-person', methods=['GET'])
@login_required
def delivery_person():
    """Delivery Person dashboard"""
    if current_user.role != User.ROLE_DELIVERY_PERSON:
        from flask import abort
        abort(403)
    
    from app.models.delivery import Delivery
    deliveries = Delivery.query.filter_by(delivery_person_id=current_user.id)\
        .order_by(Delivery.scheduled_date.desc()).limit(10).all()
    
    return render_template('dashboards/delivery_person.html', deliveries=deliveries)


@dashboard_bp.route('/admin', methods=['GET'])
@login_required
def admin():
    """Admin dashboard"""
    if current_user.role != User.ROLE_ADMIN:
        from flask import abort
        abort(403)
    
    from app.repositories.user_repository import UserRepository
    from app.repositories.audit_repository import AuditRepository
    
    user_repo = UserRepository()
    audit_repo = AuditRepository()
    
    users = user_repo.get_all()
    recent_logs = audit_repo.get_recent(7)
    
    return render_template('dashboards/admin.html', users=users, recent_logs=recent_logs)


@dashboard_bp.route('/health-safety', methods=['GET'])
@login_required
def health_safety():
    """Health & Safety Officer dashboard"""
    if current_user.role != User.ROLE_HEALTH_SAFETY_OFFICER:
        from flask import abort
        abort(403)
    
    from app.repositories.audit_repository import AuditRepository
    audit_repo = AuditRepository()
    
    recent_logs = audit_repo.get_recent(30)
    expiring_items = inventory_service.get_expiring_soon(7)
    expired_items = inventory_service.get_expired()  # Get expired items
    
    return render_template(
        'dashboards/health_safety.html',
        recent_logs=recent_logs,
        expiring_items=expiring_items,
        expired_items=expired_items
    )
