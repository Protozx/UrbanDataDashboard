# app/routes.py

from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, login_required, logout_user, current_user
from . import app, bcrypt, get_db
from .models import User

@app.route('/')
@login_required
def index():
    return render_template('index.html', name=current_user.username)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.get_by_username(username)
        if user and bcrypt.check_password_hash(user.password_hash, password):
            login_user(user)
            flash('Has iniciado sesión correctamente.', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Nombre de usuario o contraseña incorrectos.', 'danger')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if not username or not password or not confirm_password:
            flash('Por favor, completa todos los campos.', 'warning')
            return render_template('register.html')

        if password != confirm_password:
            flash('Las contraseñas no coinciden.', 'warning')
            return render_template('register.html')

        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        existing_user = cursor.fetchone()
        if existing_user:
            flash('El nombre de usuario ya está en uso.', 'danger')
            return render_template('register.html')

        password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, password_hash))
        db.commit()
        flash('Te has registrado exitosamente. Ahora puedes iniciar sesión.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión correctamente.', 'success')
    return redirect(url_for('login'))


@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    
    #return redirect(url_for('index'))
    return render_template('upload.html')
    
    
@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    
    #return redirect(url_for('index'))
    return render_template('browse.html')

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    
    #return redirect(url_for('index'))
    return render_template('upload.html')

@app.route('/view', methods=['GET', 'POST'])
def view():
    
    #return redirect(url_for('index'))
    return render_template('upload.html')