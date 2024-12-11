import os
import pandas as pd

def reduce_dataset_size(file_path, max_size_mb=10):
    """Reduce el tamaño de un dataset para que no supere un tamaño máximo en MB."""
    max_size_bytes = max_size_mb * 1024 * 1024
    if os.path.getsize(file_path) <= max_size_bytes:
        print(f"{file_path} ya está dentro del límite de {max_size_mb} MB.")
        return
    
    # Leer dataset
    dataset = pd.read_csv(file_path)
    
    # Calcular el número de registros que deben eliminarse
    current_size = os.path.getsize(file_path)
    reduction_ratio = max_size_bytes / current_size
    new_row_count = int(len(dataset) * reduction_ratio)
    
    # Reducir dataset
    reduced_dataset = dataset.sample(n=new_row_count, random_state=42)
    
    # Sobrescribir archivo con el dataset reducido
    reduced_dataset.to_csv(file_path, index=False)
    print(f"Archivo reducido: {file_path}, nuevo tamaño: {os.path.getsize(file_path) / (1024 * 1024):.2f} MB.")

# Ruta de los datasets enumerados
datasets_folder = ""  # Cambia esta ruta a donde tengas los datasets
for i in range(1, 21):
    file_path = os.path.join(datasets_folder, f"{i}.csv")
    if os.path.exists(file_path):
        reduce_dataset_size(file_path)
    else:
        print(f"{file_path} no encontrado.")
