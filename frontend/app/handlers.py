# frontend/app/handlers.py
from flask import render_template

def handle_404(error):
    return render_template('404.html'), 404

def handle_500(error):
    return render_template('500.html'), 500