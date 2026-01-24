"""
Notification controller - Handles notification routes
"""
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from flask_login import login_required, current_user
from app.services.notification_service import NotificationService

notification_bp = Blueprint('notification', __name__, url_prefix='/notifications')
notification_service = NotificationService()


@notification_bp.route('', methods=['GET'])
@login_required
def list():
    """List user notifications"""
    unread_only = request.args.get('unread', 'false').lower() == 'true'
    notifications = notification_service.get_user_notifications(current_user.id, unread_only)
    return render_template('notifications/list.html', notifications=notifications)


@notification_bp.route('/<int:notification_id>/read', methods=['PUT', 'POST'])
@login_required
def mark_read(notification_id):
    """Mark notification as read"""
    success = notification_service.mark_as_read(notification_id, current_user.id)
    
    if request.is_json or request.content_type == 'application/json':
        return jsonify({'success': success})
    
    if success:
        flash('Notification marked as read.', 'success')
    return redirect(request.referrer or url_for('notification.list'))


@notification_bp.route('/api', methods=['GET'])
@login_required
def api_list():
    """API endpoint to get notifications as JSON"""
    unread_only = request.args.get('unread', 'false').lower() == 'true'
    notifications = notification_service.get_user_notifications(current_user.id, unread_only)
    return jsonify([notif.to_dict() for notif in notifications])


@notification_bp.route('/api/unread-count', methods=['GET'])
@login_required
def api_unread_count():
    """API endpoint to get unread notification count"""
    count = notification_service.get_unread_count(current_user.id)
    return jsonify({'count': count})


@notification_bp.route('/mark-all-read', methods=['POST'])
@login_required
def mark_all_read():
    """Mark all notifications as read"""
    notification_service.mark_all_as_read(current_user.id)
    flash('All notifications marked as read.', 'success')
    return redirect(url_for('notification.list'))
