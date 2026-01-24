"""
Admin controller - Handles admin-only routes
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app.models.user import User
from app.services.auth_service import AuthService
from app.repositories.user_repository import UserRepository
from app.repositories.audit_repository import AuditRepository
from app.middleware.rbac_middleware import require_admin

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')
auth_service = AuthService()
user_repo = UserRepository()
audit_repo = AuditRepository()


@admin_bp.route('/users', methods=['GET'])
@login_required
@require_admin
def users():
    """User management page"""
    users_list = user_repo.get_all()
    return render_template('admin/users.html', users=users_list)


@admin_bp.route('/users/create', methods=['GET', 'POST'])
@login_required
@require_admin
def create_user():
    """Create new user"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        role = request.form.get('role', '')
        
        user, error = auth_service.create_user(username, email, password, role)
        
        if user:
            flash(f'User "{username}" created successfully.', 'success')
            return redirect(url_for('admin.users'))
        else:
            flash(error or 'Failed to create user.', 'error')
    
    return render_template('admin/create_user.html')


@admin_bp.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
@login_required
@require_admin
def edit_user(user_id):
    """Edit user"""
    user = user_repo.get_by_id(user_id)
    
    if not user:
        flash('User not found.', 'error')
        return redirect(url_for('admin.users'))
    
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        role = request.form.get('role', '')
        new_password = request.form.get('new_password', '').strip()
        
        # Update email
        if email and email != user.email:
            user.email = email
        
        # Update role
        if role and role != user.role:
            user.role = role
        
        # Update password if provided
        if new_password:
            from app.utils.password_hasher import hash_password
            user.password_hash = hash_password(new_password)
        
        user_repo.update(user)
        flash(f'User "{user.username}" updated successfully.', 'success')
        return redirect(url_for('admin.users'))
    
    return render_template('admin/edit_user.html', user=user)


@admin_bp.route('/users/<int:user_id>/delete', methods=['POST'])
@login_required
@require_admin
def delete_user(user_id):
    """Delete user"""
    user = user_repo.get_by_id(user_id)
    
    if not user:
        flash('User not found.', 'error')
        return redirect(url_for('admin.users'))
    
    if user.id == current_user.id:
        flash('You cannot delete your own account.', 'error')
        return redirect(url_for('admin.users'))
    
    username = user.username
    user_repo.delete(user)
    flash(f'User "{username}" deleted successfully.', 'success')
    return redirect(url_for('admin.users'))


@admin_bp.route('/audit-logs', methods=['GET'])
@login_required
@require_admin
def audit_logs():
    """View audit logs"""
    page = request.args.get('page', 1, type=int)
    per_page = 50
    offset = (page - 1) * per_page
    
    logs = audit_repo.get_all(limit=per_page, offset=offset)
    total_count = audit_repo.count()
    
    return render_template('admin/audit_logs.html', logs=logs, page=page, total_count=total_count)


@admin_bp.route('/api/audit-logs', methods=['GET'])
@login_required
@require_admin
def api_audit_logs():
    """API endpoint to get audit logs as JSON"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 50, type=int)
    offset = (page - 1) * per_page
    
    logs = audit_repo.get_all(limit=per_page, offset=offset)
    return jsonify([log.to_dict() for log in logs])
