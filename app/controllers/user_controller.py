from flask import render_template, redirect , request, jsonify, flash, url_for
from flask_login import login_user, logout_user, login_required, current_user
from . import user_bp
from app.models import user_model
from app.forms import UserForm, LoginForm


@user_bp.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('Main.dashboard')) # main page
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = user_model.get(form.username.data)
        if user and user.check_password(form.password.data):
            login_user(user,remember=form.remeber_me.data)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('Main.dashboard'))
        else:
            flash('Invalid username or password', 'danger')
            
    return render_template('users/login.html', form=form, title='Login')

@user_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('you have been logged out','info')
    return redirect(url_for('User.login'))

@user_bp.route('/sign_up', methods=['GET','POST'])
@login_required
def sign_up():
    form = UserForm(request.form)
    if request.method == 'POST' and form.validate():

        user = user_model.Users(
            username=form.username.data,
            password=form.password.data
            )
        user.add_user()
        flash('User registered successfully!', 'success')
        return redirect(url_for('User.login'))
    return render_template('users/register.html',form=form, title='Register')
        