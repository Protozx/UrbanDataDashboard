# app/init_db.py
import sqlite3
import os

DATABASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database.db')

def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Crear la tabla de usuarios
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL
        )
    ''')

    # Crear la tabla de datasets
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

    # Crear la tabla de atributos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS attributes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            dataset_id INTEGER NOT NULL,
            column_name TEXT NOT NULL,
            data_type TEXT NOT NULL,
            unit TEXT,
            FOREIGN KEY(dataset_id) REFERENCES datasets(id)
        )
    ''')

    conn.commit()
    conn.close()
    print('Base de datos inicializada.')

if __name__ == '__main__':
    init_db()
