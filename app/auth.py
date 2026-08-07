from functools import wraps
from flask import session, redirect, url_for, flash


def admin_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        if not session.get('admin_id') or session.get('role') != 'admin':
            flash('Please login as administrator.', 'warning')
            return redirect(url_for('admin.login'))
        return func(*args, **kwargs)
    return decorated
