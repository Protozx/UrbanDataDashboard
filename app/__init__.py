# app/__init__.py

from flask import Flask
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
import sqlite3
from flask import g
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'tu_clave_secreta')
app.secret_key = os.environ.get('SECRET_KEY') or 'tu_clave_secreta'

# Inicializar Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Inicializar Bcrypt
bcrypt = Bcrypt(app)






DATABASE = os.path.join(app.root_path, 'database.db')

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

from . import routes


