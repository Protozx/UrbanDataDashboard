
from .imports import *




def timeseries(request_data):          
    # Extraer los datos necesarios del JSON
    color = request_data.get('color')
    dataset_id = request_data.get('id')  # Asume que 'id' es el ID del dataset
    column_name = request_data.get('name')
    # Para decidir que funcion usar 

    if not dataset_id or not column_name:
        return jsonify({'error': 'Dataset ID and column name are required'}), 400

    # Fetch dataset path
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT id FROM datasets WHERE id = ?", (dataset_id,))
    dataset = cursor.fetchone()

    if not dataset:
        return jsonify({'error': 'Dataset not found'}), 404

    dataset_file = None
    for file in os.listdir(DATASET_DIRECTORY):
        if file.startswith(str(dataset_id)):
            dataset_file = os.path.join(DATASET_DIRECTORY, file)
            break

    if not dataset_file:
        return jsonify({'error': 'Dataset file not found'}), 404

    # Load the dataset
    import pandas as pd
    file_extension = os.path.splitext(dataset_file)[1]

    if file_extension == '.csv':
        df = pd.read_csv(dataset_file, encoding='latin-1')
    elif file_extension in ['.xlsx', '.xls']:
        df = pd.read_excel(dataset_file)
    elif file_extension == '.json':
        df = pd.read_json(dataset_file)
    elif file_extension == '.txt':
        df = pd.read_csv(dataset_file, delimiter='\t', encoding='latin-1')
    else:
        return jsonify({'error': 'Unsupported file format'}), 400

    if column_name not in df.columns:
        return jsonify({'error': f'Column {column_name} not found in dataset'}), 400

    # Limpiar valores no válidos
    values = df[column_name].dropna()  # Eliminar valores NaN
    values = values[values.apply(lambda x: isinstance(x, (int, float)))]  # Solo numéricos

    # Tomar 700 muestras representativas
    sample_size = 700
    if len(values) > sample_size:
        values = values.sample(n=sample_size, random_state=42).sort_index()
    values = values.tolist()

    return jsonify({
        'name': column_name,
        'color': color,
        'values': values
    })
    

def heatmap(request_data):          
    print("heatmap")
    # Extraer los datos necesarios del JSON
    dataset_id = request_data.get('id')  # Asume que 'id' es el ID del dataset
    column_name = request_data.get('intensity')
    x_name = request_data.get('x')
    y_name = request_data.get('y')
    
    print(dataset_id,column_name,x_name,y_name)
    # Para decidir que funcion usar 

    if not dataset_id:
        return jsonify({'error': 'Dataset ID and column name are required'}), 400

    # Fetch dataset path
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT id FROM datasets WHERE id = ?", (dataset_id,))
    dataset = cursor.fetchone()

    if not dataset:
        return jsonify({'error': 'Dataset not found'}), 404

    dataset_file = None
    for file in os.listdir(DATASET_DIRECTORY):
        if file.startswith(str(dataset_id)):
            dataset_file = os.path.join(DATASET_DIRECTORY, file)
            break

    if not dataset_file:
        return jsonify({'error': 'Dataset file not found'}), 404

    # Load the dataset
    import pandas as pd
    file_extension = os.path.splitext(dataset_file)[1]

    if file_extension == '.csv':
        df = pd.read_csv(dataset_file, encoding='latin-1')
    elif file_extension in ['.xlsx', '.xls']:
        df = pd.read_excel(dataset_file)
    elif file_extension == '.json':
        df = pd.read_json(dataset_file)
    elif file_extension == '.txt':
        df = pd.read_csv(dataset_file, delimiter='\t', encoding='latin-1')
    else:
        return jsonify({'error': 'Unsupported file format'}), 400


    # Limpiar valores no válidos
    df = df.dropna()
    
    sample_size = 1400

    if len(df) > sample_size:
        df = df.sample(n=sample_size, random_state=42).sort_index()
    
    intensity = df[column_name]
    x = df[x_name]
    y = df[y_name]
    
    #values = values[values.apply(lambda x: isinstance(x, (int, float)))]  # Solo numéricos


    return jsonify({
        'intensity': intensity.tolist(),
        'x': x.tolist(),
        'y': y.tolist()
    })
    

































