from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from . import main_bp

@main_bp.route('/')
@login_required
def index():
    return redirect(url_for('Student.list_students'))

