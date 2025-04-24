from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from functools import wraps

auth_bp = Blueprint('auth', __name__)

# Protect admin routes
def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('admin_logged_in'):
            flash('Login required.', 'warning')
            return redirect(url_for('auth.login', next=request.path))
        return f(*args, **kwargs)
    return decorated

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        u = request.form.get('username')
        p = request.form.get('password')
        if u == 'admin' and p == 'admin123':
            session['admin_logged_in'] = True
            flash('Login successful!', 'success')
            # return redirect(request.args.get('next') or url_for('admin.dashboard'))
            return redirect(request.args.get('next') or url_for('admin.admin_dashboard'))
        flash('Invalid credentials.', 'danger')
    return render_template('auth/login.html')

@auth_bp.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    flash('Logged out.', 'info')
    return redirect(url_for('auth.login'))