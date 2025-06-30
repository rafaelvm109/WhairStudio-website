from flask import Blueprint, render_template, redirect, url_for, flash, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from ..forms import RegistrationForm, LoginForm # Import LoginForm
from ..extensions import db
from ..models.user import User

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            # User exists and password is correct
            login_user(user, remember=form.remember.data)
            flash('Login bem-sucedido!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            # User does not exist or password was incorrect
            flash('Login sem sucesso. Verifique o nome de usuário e a senha.', 'danger')
    return render_template('login.html', title='Login', form=form)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # This block runs when the form is submitted and passes all validation
        hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256')
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Sua conta foi criada! Agora você pode fazer login.', 'success')
        return redirect(url_for('auth.login'))
    
    # This part runs for a GET request or if the form validation fails
    return render_template('register.html', title='Register', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))