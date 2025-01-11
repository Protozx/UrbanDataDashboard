from flask import Flask, render_template, jsonify, request
import random, os, json

app = Flask(__name__)

@app.route("/")
def home():
    # Renderizamos la página principal con el grid
    return render_template("index.html")


@app.context_processor
def inject_js_files():
    # Obtener todos los archivos .js en la carpeta 'choices'
    js_folder = os.path.join(app.static_folder, 'js', 'choices')
    js_files = [f'js/choices/{file}' for file in os.listdir(js_folder) if file.endswith('.js')]
    return {'choices_js_files': js_files}


@app.route('/query', methods=['POST'])
def handle_query():
    # Aquí puedes procesar los datos recibidos si es necesario
    # data = request.get_json()
    fakeData = {
        "labels": ["January", "February", "March", "April", "May", "June"],
        "values": [10, 20, 15, 25, 30, 45]
    }
    
    return jsonify(fakeData)



if __name__ == "__main__":
    app.run(debug=True)
