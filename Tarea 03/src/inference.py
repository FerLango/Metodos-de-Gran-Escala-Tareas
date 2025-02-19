"""
Este módulo contiene la función `make_inference` que realiza predicciones sobre los datos de 
entrada usando un modelo entrenado y guarda las predicciones en un archivo CSV.
"""

import pandas as pd
import joblib

def make_inference(input_path, model_path, output_path):
    """
    Realiza predicciones sobre los datos de entrada usando el modelo entrenado.

    Args:
        input_path (str): Ruta al archivo CSV con los datos de entrada.
        model_path (str): Ruta al archivo del modelo entrenado.
        output_path (str): Ruta donde se guardarán las predicciones en formato CSV.

    Raises:
        AttributeError: Si el modelo no contiene el atributo 'feature_names_in_' para extraer las 
        características.
    """
    try:
        # Cargar el modelo entrenado
        model = joblib.load(model_path)
    except FileNotFoundError:
        print(f"Error: El archivo del modelo '{model_path}' no se encontró.")
        return
    except joblib.externals.loky.process_executor.TerminatedWorkerError as e:
        print(f"Error al cargar el modelo: {e}")
        return

    try:
        # Cargar los datos de prueba
        test_data = pd.read_csv(input_path)
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
        # Crear una copia de los datos de prueba y generar variables dummy
        test_data_clean = test_data.copy()
        test_data_clean = pd.get_dummies(test_data_clean, drop_first=True)

        # Extraer las variables utilizadas en el entrenamiento desde el modelo
        if hasattr(model, 'feature_names_in_'):
            features = model.feature_names_in_
        else:
            raise AttributeError(
                "El modelo no contiene el atributo 'feature_names_in_' para extraer las "
                "características."
            )

        # Asegurarse de que los datos de prueba tengan las mismas columnas que los datos de
        # entrenamiento
        test_data_clean = test_data_clean.reindex(columns=features, fill_value=0)

        # Realizar predicciones
        predictions = model.predict(test_data_clean)

        # Guardar las predicciones en un DataFrame
        submission = pd.DataFrame({'Id': test_data['Id'], 'SalePrice': predictions})

        # Guardar las predicciones en un archivo CSV
        submission.to_csv(output_path, index=False)
        print(f"Predicciones guardadas en: {output_path}")

    except AttributeError as e:
        print(f"Error de atributo: {e}")
    except KeyError as e:
        print(f"Error de clave: {e}")
    except ValueError as e:
        print(f"Error durante la inferencia: {e}")

if __name__ == "__main__":
    make_inference('data/inference/test.csv', 'model/model.joblib',
                   'data/predictions/predictions.csv')
    