import os
import sqlite3
from datetime import datetime
import pandas as pd

DATASETS_FOLDER = 'app/respaldo/datasets'
CSV_PATH = 'app\scripts\datasetsIsla.csv'  # Cambia esta ruta por el archivo CSV de entrada

# Conectar a la base de datos
def get_db():
    conn = sqlite3.connect("app/database.db")
    return conn

def process_file(dataset_id, filename, cursor):
    """Procesa el archivo y guarda sus atributos en la base de datos."""
    file_path = os.path.join(DATASETS_FOLDER, filename)

    try:
        # Leer archivo con pandas y encoding latin-1
        if filename.endswith('.csv'):
            df = pd.read_csv(file_path, encoding='latin-1')
        elif filename.endswith('.xlsx'):
            df = pd.read_excel(file_path)
        elif filename.endswith('.json'):
            df = pd.read_json(file_path)
        elif filename.endswith('.txt'):
            df = pd.read_csv(file_path, delimiter='\t', encoding='latin-1')
        else:
            raise ValueError(f"Formato de archivo no soportado: {filename}")

        # Registrar atributos
        for column in df.columns:
            if pd.api.types.is_numeric_dtype(df[column]):
                data_type = 'numeric'
            else:
                data_type = 'nominal'

            cursor.execute('''
                INSERT INTO attributes (dataset_id, column_name, data_type, unit)
                VALUES (?, ?, ?, ?)
            ''', (dataset_id, column, data_type, None))

    except Exception as e:
        print(f"Error procesando archivo {filename}: {e}")

# Procesar el archivo principal
def main():
    db = get_db()
    cursor = db.cursor()

    # Leer datos del archivo CSV con encoding latin-1
    datasets_df = pd.read_csv("app/scripts/datasetsIsla.csv", encoding='utf-8-sig')

    for _, row in datasets_df.iterrows():
        #print(row)
        title = row['nombre']
        description = row['descripcion']
        tags = row['etiquetas']
        date_str = row['fecha']
        id = row['ds']

        # Parsear fecha
        try:
            upload_date = datetime.strptime(date_str, '%d-%m-%y').date()
        except ValueError:
            print(f"Fecha inválida para dataset {row['id']}: {date_str}")
            continue

        # Ruta del archivo
        filename = f"{id}.csv"
        file_path = os.path.join(DATASETS_FOLDER, filename)

        if not os.path.exists(file_path):
            print(f"Archivo no encontrado para dataset {row['id']}: {file_path}")
            continue

        # Tamaño del archivo
        file_size = os.path.getsize(file_path)

        # Insertar en la tabla datasets
        cursor.execute('''
            INSERT INTO datasets (user_id, name, description, upload_date, tag, size, has_report)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (1, title, description, upload_date, tags, file_size, 0))

        # Obtener el ID del dataset recién insertado
        dataset_id = cursor.lastrowid

        # Procesar atributos
        process_file(dataset_id, filename, cursor)

    # Confirmar cambios
    db.commit()
    db.close()

if __name__ == "__main__":
    main()
