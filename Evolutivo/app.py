from flask import Flask, render_template, jsonify, request
import random, os

app = Flask(__name__)

@app.route("/")
def home():
    # Renderizamos la página principal con el grid
    return render_template("index.html")

@app.route("/get_chart_data", methods=["POST"])
def get_chart_data():
    """
    Simula la obtención de datos para la gráfica.
    Podrías cambiar esta lógica para conectarla a una base de datos real.
    """
    chart_type = request.form.get("chartType", "")
    
    # Datos de ejemplo (simulación)
    # Podrías ajustarlos dinámicamente a tu caso de uso
    if chart_type == "bar":
        data = {
            "labels": ["Enero", "Febrero", "Marzo", "Abril", "Mayo"],
            "values": [random.randint(10, 100) for _ in range(5)]
        }
    elif chart_type == "pie":
        data = {
            "labels": ["Rojo", "Azul", "Amarillo", "Verde"],
            "values": [random.randint(10, 50) for _ in range(4)]
        }
    else:
        data = {
            "labels": [],
            "values": []
        }

    return jsonify(data)

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

    # Devuelve la palabra "Verónica"
    return jsonify("Verónica")



if __name__ == "__main__":
    app.run(debug=True)
