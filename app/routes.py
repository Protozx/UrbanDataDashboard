#app/routes.py

from .imports import *
from .plots import *


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
        titulo = request.form.get('titulo')
        descripcion = request.form.get('descripcion')
        etiquetas = request.form.get('etiquetas')
        fecha = request.form.get('fecha')
        archivo = request.files.get('archivo')

        if not titulo or not descripcion or not etiquetas or not fecha or not archivo:
            flash('Por favor, completa todos los campos.', 'warning')
            return render_template('upload.html')

        try:
            fecha_elaboracion = datetime.strptime(fecha, '%Y-%m-%d').date()
        except ValueError:
            flash('Formato de fecha inválido.', 'warning')
            return render_template('upload.html')

        nombre_original = archivo.filename
        extension = os.path.splitext(nombre_original)[1].lower()
        if extension not in ['.csv', '.xlsx', '.xls', '.txt', '.json']:
            flash('Formato de archivo no permitido.', 'warning')
            return render_template('upload.html')

        db = get_db()
        cursor = db.cursor()

        # Insertar el dataset en la tabla `datasets`
        cursor.execute('''
            INSERT INTO datasets (user_id, name, description, upload_date, tag, size, has_report)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (current_user.id, titulo, descripcion, fecha_elaboracion, etiquetas, 0, 0))
        db.commit()
        dataset_id = cursor.lastrowid

        # Guardar el archivo en el servidor
        nombre_archivo_final = f"{dataset_id}{extension}"
        ruta_archivo = os.path.join(DATASET_DIRECTORY, nombre_archivo_final)
        archivo.save(ruta_archivo)

        # Leer el archivo y registrar sus columnas como atributos
        tamanio = os.path.getsize(ruta_archivo)
        cursor.execute('UPDATE datasets SET size = ? WHERE id = ?', (tamanio, dataset_id))
        db.commit()

        try:
            import pandas as pd

            if extension == '.csv':
                df = pd.read_csv(ruta_archivo)
            elif extension in ['.xlsx', '.xls']:
                df = pd.read_excel(ruta_archivo)
            elif extension == '.json':
                df = pd.read_json(ruta_archivo)
            elif extension == '.txt':
                df = pd.read_csv(ruta_archivo, delimiter='\t')  # Suponiendo un archivo tab-delimited

            for column in df.columns:
                # Determinar el tipo de dato
                if pd.api.types.is_numeric_dtype(df[column]):
                    data_type = 'numeric'
                else:
                    data_type = 'nominal'

                # Insertar la columna como atributo en la tabla `attributes`
                cursor.execute('''
                    INSERT INTO attributes (dataset_id, column_name, data_type, unit)
                    VALUES (?, ?, ?, ?)
                ''', (dataset_id, column, data_type, None))
            db.commit()

        except Exception as e:
            flash(f'Error al procesar el archivo: {e}', 'danger')
            return render_template('upload.html')

        flash('Tu dataset se ha guardado correctamente, y sus atributos han sido registrados.', 'success')
        return redirect(url_for('index'))

    return render_template('upload.html')

   
def generar_bigrama(tags):
    # Generar bigramas a partir de una lista de tags
    # tags es una lista de tags vistos, cada dataset puede aportar varios tags
    # Ej: tags = ["ciudad", "transporte", "verde", "transporte", "carretera", ...]
    bigramas = {}
    for i in range(len(tags)-1):
        t1 = tags[i]
        t2 = tags[i+1]
        if t1 not in bigramas:
            bigramas[t1] = {}
        if t2 not in bigramas[t1]:
            bigramas[t1][t2] = 0
        bigramas[t1][t2] += 1
    return bigramas

def obtener_recomendaciones(tags_vistos, top_n=5):
    # Dado tags_vistos (lista de tags que el usuario ha visto),
    # genera un modelo bigrama y predice algunas etiquetas recomendadas.
    if len(tags_vistos) < 2:
        # No hay suficientes tags para bigramas
        return []

    bigramas = generar_bigrama(tags_vistos)
    ultimo_tag = tags_vistos[-1]
    if ultimo_tag in bigramas:
        sugerencias = sorted(bigramas[ultimo_tag].items(), key=lambda x: x[1], reverse=True)
        # sugerencias es una lista de tuplas (tag, frecuencia)
        recomendadas = [s[0] for s in sugerencias[:top_n]]
        return recomendadas
    else:
        # El último tag no tiene continuaciones en el historial
        return []


@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    db = get_db()
    cursor = db.cursor()

    search_query = ""
    if request.method == 'POST':
        search_query = request.form.get('search', '').strip()

    if search_query:
        cursor.execute('''
            SELECT datasets.id, datasets.name, datasets.description, datasets.upload_date, datasets.tag, datasets.size, users.username
            FROM datasets
            JOIN users ON datasets.user_id = users.id
            WHERE datasets.name LIKE ? OR datasets.description LIKE ? OR datasets.tag LIKE ?
            ORDER BY datasets.upload_date DESC
        ''', (f'%{search_query}%', f'%{search_query}%', f'%{search_query}%'))
    else:
        cursor.execute('''
            SELECT datasets.id, datasets.name, datasets.description, datasets.upload_date, datasets.tag, datasets.size, users.username
            FROM datasets
            JOIN users ON datasets.user_id = users.id
            ORDER BY datasets.upload_date DESC
        ''')

    datasets = cursor.fetchall()

    # Sistema de recomendación:
    # Obtenemos los tags vistos por el usuario en esta sesión
    tags_vistos = session.get('viewed_tags', [])
    recomendaciones_tags = obtener_recomendaciones(tags_vistos, top_n=5)

    # Si tenemos recomendaciones, ordenamos los datasets en base a cuántas de las etiquetas recomendadas tienen
    if recomendaciones_tags:
        def score(ds):
            # ds = (id, name, description, upload_date, tag, size, username)
            dataset_tags = ds[4].split(',')
            dataset_tags = [t.strip().lower() for t in dataset_tags]
            # Puntaje = # de tags recomendadas encontradas en este dataset
            return sum(1 for t in dataset_tags if t in recomendaciones_tags)

        # Reordenar datasets según score, mayor primero
        datasets = sorted(datasets, key=score, reverse=True)

    return render_template('browse.html', datasets=datasets, search_query=search_query, recomendaciones_tags=recomendaciones_tags)
    



@app.route('/view/<int:dataset_id>', methods=['GET', 'POST'])
@login_required
def view(dataset_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('''
        SELECT datasets.id, datasets.name, datasets.description, datasets.upload_date, datasets.tag, datasets.size, datasets.has_report, users.username
        FROM datasets
        JOIN users ON datasets.user_id = users.id
        WHERE datasets.id = ?
    ''', (dataset_id,))
    dataset = cursor.fetchone()

    if not dataset:
        flash('dataset no encontrado.', 'danger')
        return redirect(url_for('search'))

    dataset_id, name, description, upload_date, tag, size, has_report, username = dataset

    # Guardar tags en la sesión
    # tags separados por coma
    dataset_tags = [t.strip().lower() for t in tag.split(',')]
    if 'viewed_tags' not in session:
        session['viewed_tags'] = []
    session['viewed_tags'].extend(dataset_tags)

    archivo_original = None
    extension = ""
    for file in os.listdir(DATASET_DIRECTORY):
        base, ext = os.path.splitext(file)
        if base == str(dataset_id):
            archivo_original = file
            extension = ext
            break

    ruta_original = os.path.join(DATASET_DIRECTORY, archivo_original) if archivo_original else None

    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'download':
            if ruta_original and os.path.exists(ruta_original):
                return send_from_directory(DATASET_DIRECTORY, archivo_original, as_attachment=True)
            else:
                flash('archivo no encontrado.', 'danger')
                return redirect(url_for('view', dataset_id=dataset_id))

        elif action == 'report':
            flash('generando reporte, por favor espera...', 'info')
            statistics_pdf(
                str(dataset_id),
                name,
                DATASET_DIRECTORY,
                REPORT_DIRECTORY
            )
            cursor.execute('UPDATE datasets SET has_report = 1 WHERE id = ?', (dataset_id,))
            db.commit()
            flash('reporte generado con éxito.', 'success')
            return redirect(url_for('view', dataset_id=dataset_id))

        elif action == 'proccessed':
            flash('generando dataset preprocesado, por favor espera...', 'info')
            proccessed_pdf(
                str(dataset_id),
                DATASET_DIRECTORY,
                PROCESSED_DIRECTORY
            )
            flash('dataset preprocesado generado con éxito.', 'success')
            return redirect(url_for('view', dataset_id=dataset_id))

        elif action == 'download_processed':
            processed_file = f"{dataset_id}.csv"
            processed_path = os.path.join(PROCESSED_DIRECTORY, processed_file)
            if os.path.exists(processed_path):
                return send_from_directory(PROCESSED_DIRECTORY, processed_file, as_attachment=True)
            else:
                flash('dataset preprocesado no encontrado. por favor genera uno antes.', 'danger')
                return redirect(url_for('view', dataset_id=dataset_id))

    pdf_path = os.path.join(REPORT_DIRECTORY, f"{dataset_id}.pdf")
    pdf_exists = os.path.exists(pdf_path) and has_report == 1

    processed_path = os.path.join(PROCESSED_DIRECTORY, f"{dataset_id}.csv")
    processed_exists = os.path.exists(processed_path)

    return render_template('view.html', 
                           dataset_id=dataset_id, 
                           name=name, 
                           description=description, 
                           upload_date=upload_date, 
                           tag=tag, 
                           size=size, 
                           username=username, 
                           pdf_exists=pdf_exists,
                           processed_exists=processed_exists)


@app.route('/download', methods=['GET', 'POST'])
def download():
    return render_template('view.html')

@app.route('/pdf', methods=['GET', 'POST'])
def pdf_route():
    return render_template('pdf.html')

@app.route("/reports/<path:pdf_name>", methods=["GET"])
def serve_pdf(pdf_name):
    return send_from_directory("reports", pdf_name)


@app.route("/delete/<int:dataset_id>", methods=['POST'])
@login_required
def delete(dataset_id):
    db = get_db()
    cursor = db.cursor()

    action = request.form.get('action')
    if action == 'delete':
        # Verificar que el dataset pertenece al usuario actual
        cursor.execute('SELECT * FROM datasets WHERE id = ? AND user_id = ?', (dataset_id, current_user.id))
        dataset = cursor.fetchone()
        if not dataset:
            flash('Dataset no encontrado o no tienes permisos para eliminarlo.', 'danger')
            return redirect(url_for('profile'))

        # Eliminar el registro de la base de datos
        cursor.execute('DELETE FROM datasets WHERE id = ?', (dataset_id,))
        db.commit()

        # Eliminar archivos asociados
        # Eliminar archivo principal
        for file in os.listdir(DATASET_DIRECTORY):
            base, ext = os.path.splitext(file)
            if base == str(dataset_id):
                file_path = os.path.join(DATASET_DIRECTORY, file)
                if os.path.exists(file_path):
                    os.remove(file_path)
                break

        # Eliminar reporte PDF si existe
        report_file = os.path.join(REPORT_DIRECTORY, f"{dataset_id}.pdf")
        if os.path.exists(report_file):
            os.remove(report_file)

        # Eliminar dataset preprocesado si existe
        processed_file = os.path.join(PROCESSED_DIRECTORY, f"{dataset_id}.csv")
        if os.path.exists(processed_file):
            os.remove(processed_file)

        flash('Dataset eliminado correctamente.', 'success')
    else:
        flash('Acción no válida.', 'danger')

    return redirect(url_for('profile'))

@app.route("/update/<int:dataset_id>", methods=['POST'])
@login_required
def update(dataset_id):
    # Lógica para actualizar el dataset
    # Puedes redirigir a una página de edición o manejarlo aquí mismo
    flash('Dataset actualizado', 'info')
    return redirect(url_for('view', dataset_id=dataset_id))


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute('''
        SELECT datasets.id, datasets.name, datasets.description, datasets.upload_date, datasets.tag, datasets.size
        FROM datasets
        JOIN users ON datasets.user_id = users.id
        WHERE users.username = ?
        ORDER BY datasets.upload_date DESC
    ''', (current_user.username,))

            
    datasets = cursor.fetchall()        

    return render_template('profile.html', datasets=datasets)
    
def obtener_todas_etiquetas():
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT tag FROM datasets')
    etiquetas_dataset = cursor.fetchall()
    etiquetas = [etiqueta for sublist in etiquetas_dataset for etiqueta in sublist[0].split(',')]
    etiquetas = [etiqueta.strip().lower() for etiqueta in etiquetas if etiqueta.strip()]
    return obtener_recomendaciones(etiquetas, top_n=None) 



@app.context_processor
def inject_js_files():
    # Obtener todos los archivos .js en la carpeta 'choices'
    js_folder = os.path.join(app.static_folder, 'js', 'choices')
    js_files = [f'js/choices/{file}' for file in os.listdir(js_folder) if file.endswith('.js')]
    return {'choices_js_files': js_files}



@app.route('/query', methods=['POST'])
def handle_query():
    try:
        print(request)
        request_data = request.get_json()
        plot_type = request_data.get('plot')
        
        if(plot_type == "timeseries"):
            return timeseries(request_data)
        elif(plot_type == "heatmap"):
            return heatmap(request_data)
        elif(plot_type == "averagebar"):
            return averagebar(request_data)
        elif(plot_type == "gauge"):
            return gauge(request_data)
        elif(plot_type == "lasttext"):
            return lasttext(request_data)
        else:
            return jsonify({'error': 'Undefined plot type'}), 700
        
    except Exception as e:
        print("Error:", str(e))  # Depuración de errores
        return jsonify({'error': 'Internal server error'}), 500


@app.route('/dashboard')
def dashboard():
    return render_template('board.html')

@app.route('/get-datasets')
def get_datasets():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT id, name FROM datasets")
    datasets = cursor.fetchall()
    # Convertir los resultados a un formato JSON apropiado
    datasets_list = [{'id': dataset[0], 'name': dataset[1]} for dataset in datasets]
    return jsonify(datasets_list)

@app.route('/get-attributes/<int:dataset_id>')
def get_attributes(dataset_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT dataset_id, column_name, data_type, unit FROM attributes WHERE dataset_id = ?", (dataset_id,))
    attributes = cursor.fetchall()
    # Convertir los resultados a un formato JSON apropiado
    attributes_list = [{'id': attr[0],'name': attr[1], 'type': attr[2], 'unit': attr[3]} for attr in attributes]
    return jsonify(attributes_list)

