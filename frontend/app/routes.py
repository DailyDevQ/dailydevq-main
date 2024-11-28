# ./frontend/app/routes.py

from flask import Blueprint, redirect, url_for, render_template
from flask_login import logout_user
from flask_login import login_required, current_user

# Blueprint 생성
bp = Blueprint('main', __name__)

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user)