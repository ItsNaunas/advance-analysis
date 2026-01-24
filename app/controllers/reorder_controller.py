"""
Reorder controller - Handles reorder management routes
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app.services.reorder_service import ReorderService
from app.models.user import User
from app.middleware.rbac_middleware import require_role

reorder_bp = Blueprint('reorder', __name__, url_prefix='/reorders')
reorder_service = ReorderService()


@reorder_bp.route('', methods=['GET'])
@login_required
@require_role(User.ROLE_HEAD_CHEF, User.ROLE_ADMIN)
def list():
    """List all reorders"""
    reorders = reorder_service.get_all_reorders()
    return render_template('reorders/list.html', reorders=reorders)


@reorder_bp.route('/<int:reorder_id>', methods=['GET'])
@login_required
@require_role(User.ROLE_HEAD_CHEF, User.ROLE_ADMIN)
def detail(reorder_id):
    """Reorder detail page"""
    reorder = reorder_service.get_reorder(reorder_id)
    
    if not reorder:
        flash('Reorder not found.', 'error')
        return redirect(url_for('reorder.list'))
    
    return render_template('reorders/detail.html', reorder=reorder)


@reorder_bp.route('/<int:reorder_id>/confirm', methods=['POST'])
@login_required
@require_role(User.ROLE_HEAD_CHEF, User.ROLE_ADMIN)
def confirm(reorder_id):
    """Confirm reorder"""
    reorder, error = reorder_service.confirm_reorder(reorder_id, current_user.id)
    
    if reorder:
        flash('Reorder confirmed successfully.', 'success')
    else:
        flash(error or 'Failed to confirm reorder.', 'error')
    
    return redirect(url_for('reorder.list'))


@reorder_bp.route('/<int:reorder_id>/cancel', methods=['POST'])
@login_required
@require_role(User.ROLE_HEAD_CHEF, User.ROLE_ADMIN)
def cancel(reorder_id):
    """Cancel reorder"""
    reorder, error = reorder_service.cancel_reorder(reorder_id, current_user.id)
    
    if reorder:
        flash('Reorder cancelled successfully.', 'success')
    else:
        flash(error or 'Failed to cancel reorder.', 'error')
    
    return redirect(url_for('reorder.list'))


@reorder_bp.route('/generate', methods=['POST'])
@login_required
@require_role(User.ROLE_HEAD_CHEF, User.ROLE_ADMIN)
def generate():
    """Manually generate reorder (for testing)"""
    reorder = reorder_service.generate_reorder_list()
    flash(f'Reorder list generated with {len(reorder.items)} items.', 'success')
    return redirect(url_for('reorder.detail', reorder_id=reorder.id))


@reorder_bp.route('/api', methods=['GET'])
@login_required
@require_role(User.ROLE_HEAD_CHEF, User.ROLE_ADMIN)
def api_list():
    """API endpoint to get reorders as JSON"""
    reorders = reorder_service.get_all_reorders()
    return jsonify([reorder.to_dict() for reorder in reorders])
