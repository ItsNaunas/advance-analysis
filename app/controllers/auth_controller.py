"""
Authentication controller - Handles login, logout, and authentication routes
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
from flask_login import login_user, logout_user, login_required, current_user
from app.services.auth_service import AuthService
from app.middleware.rbac_middleware import require_authenticated

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
auth_service = AuthService()


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Login page and handler"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        if not username or not password:
            flash('Please provide both username and password.', 'error')
            return render_template('auth/login.html')
        
        user, error = auth_service.authenticate(username, password)
        
        if user:
            login_user(user, remember=True)
            next_page = request.args.get('next') or url_for('dashboard.index')
            flash(f'Welcome back, {user.username}!', 'success')
            return redirect(next_page)
        else:
            flash(error or 'Invalid username or password.', 'error')
    
    return render_template('auth/login.html')


@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    """Logout handler"""
    logout_user()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('auth.login'))


@auth_bp.route('/api/login', methods=['POST'])
def api_login():
    """API endpoint for login (for AJAX)"""
    data = request.get_json()
    username = data.get('username', '').strip()
    password = data.get('password', '')
    
    if not username or not password:
        return jsonify({'success': False, 'error': 'Username and password required'}), 400
    
    user, error = auth_service.authenticate(username, password)
    
    if user:
        login_user(user, remember=True)
        return jsonify({
            'success': True,
            'user': {
                'id': user.id,
                'username': user.username,
                'role': user.role
            }
        })
    else:
        return jsonify({'success': False, 'error': error or 'Invalid credentials'}), 401


@auth_bp.route('/api/me', methods=['GET'])
@login_required
def api_me():
    """API endpoint to get current user info"""
    return jsonify({
        'id': current_user.id,
        'username': current_user.username,
        'email': current_user.email,
        'role': current_user.role
    })
