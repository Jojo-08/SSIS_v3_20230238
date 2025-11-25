from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from . import main_bp

@main_bp.route('/')
@login_required
def dashboard():
    return render_template('dashboard.html',title='Dashboard')

@main_bp.route('/settings')
@login_required
def settings():
    return render_template('settings.html',title='Settings')

