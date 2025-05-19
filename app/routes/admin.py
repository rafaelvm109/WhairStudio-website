from flask import Blueprint, render_template

admin = Blueprint('admin', __name__)

@admin.route('/dashboard')
def dashboard():
    return render_template('admin/dashboard.html')