from flask import render_template, redirect, request, jsonify, flash, url_for
from flask_login import login_user, logout_user, login_required, current_user

from . import user_bp
from app.models.user_model import User
from app.forms import UserForm, LoginForm


@user_bp.route('/login', methods=['GET','POST'])
def login():
    # If user is already logged in, redirect to dashboard
    if current_user.is_authenticated:
        return redirect(url_for('Main.dashboard'))
    
    form = LoginForm()

    if form.validate_on_submit():
        user = User.get(form.username.data)

        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            flash('Logged in successfully!', 'success')
            
            # Redirect to next page if it exists, otherwise to dashboard
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('Main.dashboard'))
        else:
            flash('Invalid username or password', 'danger')
            
    return render_template('login.html', form=form, title='Login')

@user_bp.route('/logout')
def logout():
    logout_user()
    flash('you have been logged out','info')
    return redirect(url_for('User.login'))

@user_bp.route('/sign_up', methods=['GET','POST'])
def sign_up():
    # If user is already logged in, redirect to dashboard
    if current_user.is_authenticated:
        return redirect(url_for('Main.dashboard'))
    
    form = UserForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data
        )
        if user.add_user():
            flash('User registered successfully! Please log in.', 'success')
            return redirect(url_for('User.login'))
        else:
            flash('Error creating user. Username or email might already exist.', 'danger')
    return render_template('register.html', form=form, title='Register')
        