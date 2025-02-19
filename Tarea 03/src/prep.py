"""
Este módulo contiene la función `prepare_data` que preprocesa los datos de entrada y guarda los 
datos procesados.
"""

import pandas as pd
from utils import clean_data, feature_selection

def prepare_data(input_path, output_path):
    """
    Preprocesa los datos de entrada y guarda los datos procesados.

    Args:
        input_path (str): Ruta al archivo CSV con los datos de entrada.
        output_path (str): Ruta donde se guardarán los datos procesados en formato CSV.
    """
    try:
        # Cargar los datos
        train = pd.read_csv(input_path)
    except FileNotFoundError:
        print(f"Error: El archivo de entrada '{input_path}' no se encontró.")
    except pd.errors.EmptyDataError:
        print(f"Error: El archivo de entrada '{input_path}' está vacío.")
    except pd.errors.ParserError as e:
        print(f"Error al leer el archivo de entrada: {e}")

    try:
        # Limpiar los datos
        train_clean = clean_data(train)
    except KeyError as e:
        print(f"Error de clave durante la limpieza de datos: {e}")
    except ValueError as e:
        print(f"Error de valor durante la limpieza de datos: {e}")

    try:
        # Seleccionar características importantes
        selected_features = feature_selection(train_clean)
        selected_features.append('SalePrice')
        train_final = train_clean[selected_features]
    except KeyError as e:
        print(f"Error de clave: {e}")
    except ValueError as e:
        print(f"Error durante la selección de características: {e}")

    try:
        # Guardar el dataset procesado
        train_final.to_csv(output_path, index=False)
        print(f"Datos procesados guardados en: {output_path}")
    except IOError as e:
        print(f"Error al guardar los datos procesados: {e}")

if __name__ == "__main__":
    prepare_data('data/raw/train.csv', 'data/prep/train_clean.csv')
    