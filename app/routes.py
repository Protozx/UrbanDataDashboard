# app/routes.py

from flask import render_template, redirect, url_for, flash, request, abort, send_from_directory
from flask_login import login_user, login_required, logout_user, current_user
from . import app, bcrypt, get_db
from .models import User
import os as os
from datetime import datetime

DATASET_DIRECTORY = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'datasets')
if not os.path.exists(DATASET_DIRECTORY):
    os.makedirs(DATASET_DIRECTORY)


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
    if request.method == 'POST':
        # Obtenemos los datos del formulario
        titulo = request.form.get('titulo')
        descripcion = request.form.get('descripcion')
        etiquetas = request.form.get('etiquetas')
        fecha = request.form.get('fecha')
        archivo = request.files.get('archivo')

        # Validamos que existan datos obligatorios
        if not titulo or not descripcion or not etiquetas or not fecha or not archivo:
            flash('Todos los campos son obligatorios.', 'warning')
            return render_template('upload.html')

        # Convertimos la fecha a un formato manejable
        try:
            fecha_elaboracion = datetime.strptime(fecha, '%Y-%m-%d').date()
        except ValueError:
            flash('Formato de fecha inválido.', 'warning')
            return render_template('upload.html')

        # Verificamos si el archivo es permitido (por ejemplo, .csv)
        # Esto es opcional, se puede omitir o ajustar
        nombre_original = archivo.filename
        extension = os.path.splitext(nombre_original)[1].lower()
        if extension not in ['.csv', '.xlsx', '.xls', '.txt', '.json']:
            flash('Formato de archivo no permitido.', 'warning')
            return render_template('upload.html')

        # Insertamos primero el registro en la base de datos sin el ID del archivo
        db = get_db()
        cursor = db.cursor()
        # has_report y size se pueden manejar ahora o después
        # Aquí, asumimos que has_report es False (0) inicialmente
        # size se calculará después de guardar el archivo
        cursor.execute('''
            INSERT INTO datasets (user_id, name, description, upload_date, tag, size, has_report)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (current_user.id, titulo, descripcion, fecha_elaboracion, etiquetas, 0, 0))
        db.commit()
        dataset_id = cursor.lastrowid

        # Guardamos el archivo con el nombre del dataset_id
        nombre_archivo_final = f"{dataset_id}{extension}"
        ruta_archivo = os.path.join(DATASET_DIRECTORY, nombre_archivo_final)
        archivo.save(ruta_archivo)

        # Ahora que tenemos el archivo guardado, obtenemos su tamaño
        tamanio = os.path.getsize(ruta_archivo)
        # Actualizamos la base de datos con el tamaño
        cursor.execute('UPDATE datasets SET size = ? WHERE id = ?', (tamanio, dataset_id))
        db.commit()

        flash('Tu dataset se ha guardado correctamente.', 'success')
        return redirect(url_for('index'))

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
    return render_template('profile.html')

@app.route('/view', methods=['GET', 'POST'])
def view():
    
    #return redirect(url_for('index'))
    return render_template('view.html')


@app.route('/download', methods=['GET', 'POST'])
def download():
    
    #return redirect(url_for('index'))
    return render_template('view.html')

@app.route('/pdf', methods=['GET', 'POST'])
def pdf_route():
    
    #return redirect(url_for('index'))
    return render_template('pdf.html')

PDF_DIRECTORY = "./datasets"

@app.route("/reports/<path:pdf_name>", methods=["GET"])
def serve_pdf(pdf_name):
    # Cambia './datasets' por la ruta absoluta si es necesario
    return send_from_directory("reports", pdf_name)
