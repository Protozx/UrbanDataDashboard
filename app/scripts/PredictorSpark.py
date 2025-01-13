import os
import sqlite3
from datetime import datetime

# pandas y pyspark
import pandas as pd
from pyspark.sql import SparkSession
from pyspark import SparkConf
from pyspark.sql.functions import col, when, lit, regexp_replace
from pyspark.sql import functions as F
from pyspark.sql.types import StringType
from pyspark.ml.feature import Imputer, Tokenizer, NGram
from pyspark.ml import Pipeline

# carpeta donde se encuentran los datasets
DATASETS_FOLDER = 'app/respaldo/datasets'
# ruta de tu archivo csv con la información principal
CSV_PATH = 'app/scripts/datasetsIsla.csv'

#############################
#  1. CONEXIÓN A LA BD
#############################

def get_db():
    """
    Obtiene una conexión sqlite3 a la base de datos 'app/database.db'.
    """
    conn = sqlite3.connect("app/database.db")
    return conn

#############################
#  2. FUNCIÓN PARA PROCESAR ARCHIVO Y REGISTRAR ATRIBUTOS
#############################

def process_file(dataset_id, filename, cursor):
    """
    Procesa el archivo para extraer sus columnas y tipos de dato,
    registrando dichos atributos en la tabla 'attributes' de la BD.
    """
    file_path = os.path.join(DATASETS_FOLDER, filename)

    try:
        # leer el archivo con pandas y encoding latin-1, según la extensión
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

        # registrar atributos
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

#############################
#  3. PROCESO PRINCIPAL
#############################

def main():
    # 3.1 iniciar o crear la base de datos
    db = get_db()
    cursor = db.cursor()

    # 3.2 leer los metadatos del csv principal (datasetsIsla.csv) con pandas
    # se usa 'utf-8-sig' para evitar problemas con encabezados
    datasets_df = pd.read_csv(CSV_PATH, encoding='utf-8-sig')

    for _, row in datasets_df.iterrows():
        title = row['nombre']
        description = row['descripcion']
        tags = row['etiquetas']
        date_str = row['fecha']
        ds_id = row['ds']  # id del dataset en tu csv

        # parsear fecha (formato 'dd-mm-yy')
        try:
            upload_date = datetime.strptime(date_str, '%d-%m-%y').date()
        except ValueError:
            print(f"Fecha inválida para dataset {row['id']}: {date_str}")
            continue

        # construir la ruta real del archivo (asumiendo que son .csv)
        filename = f"{ds_id}.csv"
        file_path = os.path.join(DATASETS_FOLDER, filename)

        if not os.path.exists(file_path):
            print(f"Archivo no encontrado para dataset {row['id']}: {file_path}")
            continue

        # tamaño del archivo en bytes
        file_size = os.path.getsize(file_path)

        # insertar en la tabla 'datasets'
        cursor.execute('''
            INSERT INTO datasets (user_id, name, description, upload_date, tag, size, has_report)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (1, title, description, upload_date, tags, file_size, 0))

        # obtener el id del dataset recién insertado
        dataset_id = cursor.lastrowid

        # procesar el archivo para extraer columnas y tipos de dato
        process_file(dataset_id, filename, cursor)

    # confirmar los cambios en base de datos
    db.commit()
    db.close()

    #############################################
    #  3.3 ENTRENAR MODELO DE PREDICCIÓN EN SPARK
    #############################################

    # configuración de spark para aprovechar workers
    conf = SparkConf() \
        .setAppName("RellenoValoresFaltantesMatrizEvolutivaConEnegramas") \
        .set("spark.executor.instances", "4") \
        .set("spark.executor.memory", "2g") \
        .set("spark.executor.cores", "2")

    spark = SparkSession.builder.config(conf=conf).getOrCreate()

    spark_file_path = os.path.join(DATASETS_FOLDER, "ds000.csv")
    if not os.path.exists(spark_file_path):
        print(f"No se encontró {spark_file_path}, finalizamos el modelo spark.")
        spark.stop()
        return

    # leemos el dataset con spark
    df_spark = spark.read.csv(spark_file_path, header=True, inferSchema=True)

    columnas_numericas = []
    columnas_texto = []

    for nombre, tipo in df_spark.dtypes:
        # solo para ejemplo: si es 'int' o 'double', lo consideramos numérico
        if tipo in ["int", "double", "float", "long"]:
            columnas_numericas.append(nombre)
        else:
            columnas_texto.append(nombre)

    # 3.3.1: imputación de valores faltantes en columnas numéricas
    if columnas_numericas:
        # creamos un imputador para reemplazar nulos con la media
        imputer = Imputer(
            inputCols=columnas_numericas,
            outputCols=[col + "_imputado" for col in columnas_numericas]
        ).setStrategy("mean")
    else:
        imputer = None

    # 3.3.2: tokenización de columnas de texto y enegramas
    #       (similar a n-gramas: bigramas, trigramas, etc.)
    etapas_tokenizacion = []
    for col_text in columnas_texto:
        # 1) limpiar texto (ejemplo eliminar caracteres raros, saltos de línea, etc.)
        #    usaremos una columna temporal col_text + "_limpio"
        df_spark = df_spark.withColumn(
            col_text + "_limpio", 
            regexp_replace(col(col_text).cast(StringType()), "[^a-zA-Z0-9áéíóúÁÉÍÓÚñÑ ]", "")
        )

        # 2) tokenizer para generar tokens
        tokenizer = Tokenizer(
            inputCol=col_text + "_limpio", 
            outputCol=col_text + "_tokens"
        )
        # 3) enegramas (en este ejemplo haremos bigramas)
        #    puedes ajustar el parámetro n según tu interés
        ngram = NGram(n=2, inputCol=col_text + "_tokens", outputCol=col_text + "_enegramas")

        etapas_tokenizacion.extend([tokenizer, ngram])

    # armamos el pipeline con los pasos que tengamos (imputador + tokenización)
    etapas_pipeline = []
    if imputer:
        etapas_pipeline.append(imputer)
    if etapas_tokenizacion:
        etapas_pipeline.extend(etapas_tokenizacion)

    # si no hay columnas numéricas ni texto, no hacemos nada
    if not etapas_pipeline:
        print("No se encontraron columnas numéricas ni de texto para procesar.")
        spark.stop()
        return

    pipeline = Pipeline(stages=etapas_pipeline)

    # entrenamos el pipeline (la carga se reparte en los workers)
    modelo = pipeline.fit(df_spark)

    # transformamos el df original, generando las columnas imputadas y enegramas
    df_procesado = modelo.transform(df_spark)

    # mostramos algunas filas para verificar
    df_procesado.show(truncate=False)

    
    df_procesado.write.parquet("ruta/salida", mode="overwrite")

    # cerramos la sesión spark
    spark.stop()

#############################
#  EJECUCIÓN DEL SCRIPT
#############################

if __name__ == "__main__":
    main()
