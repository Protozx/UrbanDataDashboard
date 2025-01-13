
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
    sample_size = 2000
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
    center = [x.mean(), y.mean()]
    
    #values = values[values.apply(lambda x: isinstance(x, (int, float)))]  # Solo numéricos


    return jsonify({
        'intensity': intensity.tolist(),
        'x': x.tolist(),
        'y': y.tolist(),
        'max_intensity': intensity.max(),
        'min_intensity': intensity.min(),
        'center': center
    })
    




def averagebar(request_data):          
    print("average bar")
    # Extraer los datos necesarios del JSON
    dataset_id = request_data.get('id')  # Asume que 'id' es el ID del dataset
    values_column = request_data.get('values')
    labels_column = request_data.get('tags')
    

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
    
    aggregated_df = df.groupby(labels_column)[values_column].mean().reset_index()

    values = aggregated_df[values_column]
    labels = aggregated_df[labels_column]

    return jsonify({
        'values': values.tolist(),
        'labels': labels.tolist()
    })
    

def lasttext(request_data):          
    print("lasttext")
    # Extraer los datos necesarios del JSON
    dataset_id = request_data.get('id')  # Asume que 'id' es el ID del dataset
    column = request_data.get('column')
    color = request_data.get('color')
    

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
    df = df.dropna()
    reading = df.iloc[-1][column]
    
    return jsonify({
        'color': color,
        'reading': reading
    })


def gauge(request_data):          
    print("gauge")
    # Extraer los datos necesarios del JSON
    dataset_id = request_data.get('id')  # Asume que 'id' es el ID del dataset
    column = request_data.get('column')
    

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
    df = df.dropna()
    reading = df.iloc[-1][column]

    
    print(reading.tolist(), reading);
    
    return jsonify({
        'reading': round(reading, 1),
        'min_value': request_data.get('min_value'),
        'max_value': request_data.get('max_value'),
        'color': request_data.get('color')
    })


def statistic(request_data):          
    
    # Extraer los datos necesarios del JSON
    dataset_id = request_data.get('id')  # Asume que 'id' es el ID del dataset
    column_1 = request_data.get('column_1')
    column_2 = request_data.get('column_2')
    statistic_name = request_data.get('statistic')
    print(statistic_name)
    

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
    resultado = 0
    value_2 = "None"
    
    
    if statistic_name == "Max":
        resultado = df[column_1].max()
        if column_2 != "None":
            value_2 = df.loc[df[column_1] == resultado, column_2].iloc[0]
    elif statistic_name == "Min":
        resultado = df[column_1].min()
        if column_2 != "None":
            value_2 = df.loc[df[column_1] == resultado, column_2].iloc[0]
    elif statistic_name == "Mean":
        resultado = df[column_1].mean()
    elif statistic_name == "Median":
        resultado = df[column_1].median()
    elif statistic_name == "Mode":
        resultado = df[column_1].mode().iloc[0]  # Devuelve el primer modo si hay varios
    elif statistic_name == "Variance":
        resultado = df[column_1].var()
    else:
        resultado = "Estadística no reconocida."

    
    value_1 = round(resultado, 1)
    
    if value_2 == "None":
        graph = 1
    else: 
        graph = 2
    
    
    

    return jsonify({
        'statistic': statistic_name,
        'value_1': value_1.tolist(),
        'value_2': value_2,
        'graph': graph,
        'color': request_data.get('color'),
        'column_1': column_1,
        'column:2': column_2
    })
 






























