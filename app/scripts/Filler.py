import csv
import sqlite3
import os

DATABASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database.db')

def load_datasets():
    conn = sqlite3.connect("app/database.db")
    cursor = conn.cursor()

    # Asegurarse de que la tabla existe
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS datasets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            description TEXT,
            upload_date DATE NOT NULL,
            tag TEXT,
            size REAL,
            has_report BOOLEAN NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')

    # Abrir el archivo CSV y asegurar que la codificación sea la correcta
    with open('app/scripts/datasetsIsla.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Insertar datos en la tabla datasets
            cursor.execute('''
                INSERT INTO datasets (user_id, name, description, upload_date, tag, size, has_report) 
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (2, row['nombre'], row['descripcion'], row['fecha'], row['etiquetas'], 0.0, 0))

    conn.commit()
    conn.close()
    print('Datos cargados en la base de datos.')

if __name__ == '__main__':
    load_datasets()
