"""
Este módulo contiene la función `train_model` que entrena un modelo utilizando los datos de entrada
y guarda el modelo entrenado.
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import argparse

def train_model(input_path, model_output_path):
    """
    Entrena un modelo utilizando los datos de entrada y guarda el modelo entrenado.

    Args:
        input_path (str): Ruta al archivo CSV con los datos de entrada.
        model_output_path (str): Ruta donde se guardará el modelo entrenado.
    """
    try:
        # Cargar los datos procesados
        train_data = pd.read_csv(input_path)
    except FileNotFoundError:
        print(f"Error: El archivo de entrada '{input_path}' no se encontró.")
        return
    except pd.errors.EmptyDataError:
        print(f"Error: El archivo de entrada '{input_path}' está vacío.")
        return
    except pd.errors.ParserError as e:
        print(f"Error al leer el archivo de entrada: {e}")
        return

    try:
        # Preparar los datos
        features = train_data.drop(columns=['SalePrice'])
        features = pd.get_dummies(features, drop_first=True)
        target = train_data['SalePrice']

        # Dividir los datos en entrenamiento y validación
        features_train, features_val, target_train, target_val = train_test_split(
            features, target, test_size=0.2, random_state=42
        )

        # Entrenar el modelo RandomForest
        model = RandomForestRegressor(random_state=42)
        model.fit(features_train, target_train)
    except KeyError as e:
        print(f"Error de clave: {e}")
        return
    except ValueError as e:
        print(f"Error durante la preparación de datos o el entrenamiento del modelo: {e}")
        return

    try:
        # Guardar el modelo entrenado
        joblib.dump(model, model_output_path)
        print(f"Modelo entrenado guardado en: {model_output_path}")
    except IOError as e:
        print(f"Error al guardar el modelo: {e}")
        return

    try:
        # Evaluación del modelo
        target_pred = model.predict(features_val)
        mse = mean_squared_error(target_val, target_pred)
        rmse = np.sqrt(mse)
        r2 = r2_score(target_val, target_pred)

        print(f"RMSE: {rmse:.2f}")
        print(f"R2 Score: {r2:.2f}")
    except ValueError as e:
        print(f"Error durante la evaluación del modelo: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Entrenar un modelo de Machine Learning')
    parser.add_argument("--input_path", type=str, default="data/prep/train_clean.csv",
                        help="Ruta al archivo CSV de datos de entrada")
    parser.add_argument("--model_output_path", type=str, default="model/model.joblib",
                        help="Ruta donde se guardará el modelo entrenado")
    args = parser.parse_args()
    
    train_model(args.input_path, args.model_output_path)
    