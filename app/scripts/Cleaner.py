import pandas as pd
from collections import defaultdict
import random
import numpy as np
import os

def levenshtein_distance(a, b):
    if a is None: a = ""
    if b is None: b = ""
    a, b = str(a), str(b)
    m, n = len(a), len(b)
    dp = [[0]*(n+1) for _ in range(m+1)]
    for i in range(m+1):
        dp[i][0] = i
    for j in range(n+1):
        dp[0][j] = j
    for i in range(1, m+1):
        for j in range(1, n+1):
            cost = 0 if a[i-1] == b[j-1] else 1
            dp[i][j] = min(
                dp[i-1][j] + 1,
                dp[i][j-1] + 1,
                dp[i-1][j-1] + cost
            )
    return dp[m][n]

def is_numeric(value):
    try:
        float(value)
        return True
    except:
        return False

def calculate_distance(key1, key2):
    dist = 0.0
    # Distancia entre dos tuplas
    for x, y in zip(key1, key2):
        if is_numeric(x) and is_numeric(y):
            dist += (float(x) - float(y))**2
        else:
            dist += levenshtein_distance(str(x), str(y))
    # Si todos eran numéricos, se usa la raíz (euclídea)
    if all(is_numeric(val) for val in key1+key2):
        dist = dist**0.5
    return dist

def generate_ngrams(data, n):
    ngrams = defaultdict(list)
    for i in range(len(data) - n + 1):
        key = tuple(data[i:i+n-1])
        ngrams[key].append(data[i+n-1])
    return ngrams

def consensus_based_prediction(predictions, fallback_value):
    if not predictions:
        return fallback_value
    if all(is_numeric(p) for p in predictions):
        vals = [float(p) for p in predictions]
        mean = np.mean(vals)
        std_dev = np.std(vals)
        filtered = [float(p) for p in vals if abs(p - mean) <= std_dev]
        resultado = np.mean(filtered) if filtered else mean
        return resultado
    else:
        from collections import Counter
        freq = Counter(predictions)
        resultado = freq.most_common(1)[0][0] if freq else fallback_value
        return resultado

def find_closest_key(model, key):
    return min(model.keys(), key=lambda k: calculate_distance(k, key))

def predict_next_value(model, last_values, num_predictions=10):
    key = tuple(last_values)
    if key not in model:
        if len(model) == 0:
            # Sin modelo, devolvemos el fallback como None
            return [None]*num_predictions
        closest_key = find_closest_key(model, key)
        key = closest_key
    predictions = [random.choice(model[key]) for _ in range(num_predictions)]
    return predictions

def fill_missing_values_in_column(df, column, n=3, prediction_steps=1):
    """
    Esta función llenará los valores faltantes en la columna dada usando el predictor n-gram definido arriba.
    - Convirtirá '?' a NaN.
    - Entrenará un modelo ngram con los valores conocidos.
    - Luego intentará predecir y llenar los valores faltantes de forma secuencial.
    """
    # Convertir los '?' a NaN y trabajar con una lista
    col_data = df[column].replace('?', np.nan)
    col_data = col_data.tolist()

    # Separar datos conocidos y desconocidos
    known_data = [x for x in col_data if pd.notna(x)]

    # Si no hay datos conocidos, no podemos predecir nada, quizás dejar todo como NaN
    if len(known_data) == 0:
        return df

    # Entrenar el modelo con los datos conocidos
    # Para ello necesitamos una serie continua sin NaN
    # Vamos a ignorar las filas con NaN al entrenar
    training_data = [x for x in col_data if pd.notna(x)]
    if len(training_data) < n:
        # Muy pocos datos para entrenar
        # No podemos predecir con ngram, dejamos como estan
        return df

    model = generate_ngrams(training_data, n)

    # Ahora iteramos sobre la columna y cuando encontremos NaN, intentamos predecir
    # Para predecir, necesitamos el contexto (los últimos n-1 valores antes del faltante)
    for i in range(len(col_data)):
        if pd.isna(col_data[i]):
            # Buscar último contexto disponible de tamaño n-1 hacia atrás
            # Si no hay suficiente contexto, usar los datos conocidos más cercanos
            context_start = i - (n - 1)
            if context_start < 0:
                # Sin contexto suficiente al inicio, usamos cualquiera que tengamos
                # Por ejemplo, repetir el primer valor conocido o fallback simple.
                # Aquí elegiremos el valor medio de los datos conocidos como fallback.
                fallback_value = np.mean([float(x) for x in known_data if is_numeric(x)]) if all(is_numeric(x) for x in known_data) else known_data[0]
                # Predicción sin contexto no es posible, asignar fallback
                col_data[i] = fallback_value
                continue

            # Construir el contexto
            last_values = col_data[context_start:i]
            # Si hay NaN en el contexto, intentar retroceder más o saltar
            # Simplificamos: si el contexto tiene NaN, no se puede predecir. Buscamos el contexto conocido más cercano
            # Si no logramos contexto limpio, usamos fallback
            if any(pd.isna(x) for x in last_values):
                # Buscar el último tramo n-1 antes de i sin NaN
                for shift_back in range(1, i+1):
                    if i - (n-1) - shift_back < 0:
                        # Sin contexto posible
                        fallback_value = np.mean([float(x) for x in known_data if is_numeric(x)]) if all(is_numeric(x) for x in known_data) else known_data[0]
                        col_data[i] = fallback_value
                        break
                    candidate_context = col_data[i-(n-1)-shift_back : i-shift_back]
                    if len(candidate_context) == n-1 and all(pd.notna(x) for x in candidate_context):
                        last_values = candidate_context
                        break
                else:
                    # Si no se rompió el for, no encontramos contexto
                    fallback_value = np.mean([float(x) for x in known_data if is_numeric(x)]) if all(is_numeric(x) for x in known_data) else known_data[0]
                    col_data[i] = fallback_value
                    continue

            # Ahora last_values es el contexto limpio
            # Predecir el valor faltante
            next_predictions = predict_next_value(model, last_values, num_predictions=10)

            # Definir fallback si no hay predicción válida
            fallback_value = np.mean([float(x) for x in known_data if is_numeric(x)]) if all(is_numeric(x) for x in known_data) else known_data[0]

            predicted_value = consensus_based_prediction(next_predictions, fallback_value)
            col_data[i] = predicted_value

            # Actualizar el modelo con el nuevo valor predicho
            if len(last_values) == n-1:
                key = tuple(last_values)
                if key not in model:
                    model[key] = []
                model[key].append(predicted_value)

    # Reemplazar la columna en el dataframe
    df[column] = col_data
    return df

def proccessed_pdf(input_csv, output_folder="app/datasets/proccessed"):
    # Cargar el dataset
    input_path = os.path.join("app/datasets", (input_csv + ".csv"))
    df = pd.read_csv(input_path)

    # Parametros del predictor
    n = 3
    prediction_steps = 1

    # Por cada columna, verificar valores faltantes y '?'
    for col in df.columns:
        if df[col].isna().any() or (df[col] == '?').any():
            df = fill_missing_values_in_column(df, col, n=n, prediction_steps=prediction_steps)

    # Guardar el dataset limpio
    # Si el output_folder no existe, crearlo
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    output_path = os.path.join(output_folder, (input_csv + ".csv"))
    df.to_csv(output_path, index=False)
    print("Archivo limpio guardado en:", output_path)

if __name__ == "__main__":
    proccessed_pdf("16")
    
