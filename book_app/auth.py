from flask import Blueprint, render_template, request, redirect, url_for, flash
from .dbmodels import User, db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required

auth = Blueprint('auth', __name__)

@auth.route('/signup', methods=['GET', 'POST'])
def signup():

    if request.method == 'POST':

        email = request.form.get('email')
        password = request.form.get('password')

        #EMAIL VALIDATION
        if '@' not in email or '.' not in email:
            flash("Please enter a valid email address", "danger")
            return redirect(url_for('auth.signup'))

        #PASSWORD LENGTH VALIDATION
        if len(password) < 6:
            flash("Password must be at least 6 characters", "danger")
            return redirect(url_for('auth.signup'))

        #CHECK EXISTING USER
        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            flash("Email already registered", "danger")
            return redirect(url_for('auth.signup'))

        # CREATE USER
        new_user = User(
            email=email,
            password=generate_password_hash(password)
        )

        db.session.add(new_user)
        db.session.commit()

        flash("Account created successfully!", "success")

        return redirect(url_for('auth.login'))

    return render_template('signup.html')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password, password):
            flash('Invalid credentials')
            return redirect(url_for('auth.login'))

        login_user(user)
        
        flash("Login successful", "success")
        next_page = request.args.get('next')
        return redirect(url_for('main.index'))

    return render_template('login.html')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))