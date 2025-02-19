"""
Este módulo contiene funciones de utilidad para la limpieza de datos y la selección de 
características.
"""

import numpy as np
from scipy.stats import f_oneway

def clean_data(df):
    """
    Limpia los datos: elimina columnas innecesarias y maneja los valores nulos.

    Args:
        df (pd.DataFrame): DataFrame con los datos a limpiar.

    Returns:
        pd.DataFrame: DataFrame limpio.
    """
    try:
        # Eliminar la columna 'Id'
        df_clean = df.copy().drop(columns=['Id'])

        # Rellenar los valores nulos
        numerical_cols = df_clean.select_dtypes(include=['number']).columns.tolist()
        categorical_cols = df_clean.select_dtypes(include=['object']).columns.tolist()

        df_clean[numerical_cols] = df_clean[numerical_cols].fillna(0)
        df_clean[categorical_cols] = df_clean[categorical_cols].fillna("None")

        return df_clean
    except KeyError as e:
        print(f"Error de clave: {e}")
        return None
    except ValueError as e:
        print(f"Error durante la limpieza de datos: {e}")
        return None

def categorical_feature_selection(df, p_value_threshold=0.01):
    """
    Selecciona las características categóricas más relevantes para el modelo mediante ANOVA.

    Args:
        df (pd.DataFrame): DataFrame con los datos.
        p_value_threshold (float): Umbral de valor p para la selección de características.

    Returns:
        list: Lista de características categóricas seleccionadas.
    """
    try:
        categorical_features = df.select_dtypes(include=['object', 'category']).columns
        anova_results = {}

        for feature in categorical_features:
            categories = df[feature].unique()
            groups = [df[df[feature] == category]['SalePrice'] for category in categories]
            f_statistic, p_value = f_oneway(*groups)
            anova_results[feature] = (f_statistic, p_value)

        categorical_selected = {
            feature: (f_stat, p_val) for feature, (f_stat, p_val) in anova_results.items()
            if p_val < p_value_threshold
        }
        categorical_selected = list(categorical_selected.keys())

        return categorical_selected
    except KeyError as e:
        print(f"Error de clave: {e}")
        return []
    except ValueError as e:
        print(f"Error durante la selección de características categóricas: {e}")
        return []

def numerical_feature_selection(df, strong_corr_threshold=0.3, ind_corr_threshold=0.8):
    """
    Selecciona las características numéricas más relevantes para el modelo mediante correlación.

    Args:
        df (pd.DataFrame): DataFrame con los datos.
        strong_corr_threshold (float): Umbral de correlación fuerte con la variable objetivo.
        independent_corr_threshold (float): Umbral de correlación independiente entre 
                                            características.

    Returns:
        list: Lista de características numéricas seleccionadas.
    """
    try:
        corr = df.select_dtypes(include=['int64', 'float64']).corr()
        strong_corr = corr[corr['SalePrice'].abs() > strong_corr_threshold]['SalePrice']
        strong_corr = strong_corr.sort_values(ascending=False).drop('SalePrice')
        corr_matrix = df[strong_corr.index].corr().abs()
        upper = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))
        to_drop = [column for column in upper.columns if any(upper[column] > ind_corr_threshold)]
        numerical_selected = [col for col in strong_corr.index if col not in to_drop]

        return numerical_selected
    except KeyError as e:
        print(f"Error de clave: {e}")
        return []
    except ValueError as e:
        print(f"Error durante la selección de características numéricas: {e}")
        return []

def feature_selection(df):
    """
    Selecciona las características más relevantes para el modelo.

    Args:
        df (pd.DataFrame): DataFrame con los datos.

    Returns:
        list: Lista de características seleccionadas.
    """
    try:
        numerical_features = numerical_feature_selection(df)
        categorical_features = categorical_feature_selection(df)
        selected_features = numerical_features + categorical_features

        return selected_features
    except ValueError as e:
        print(f"Error durante la selección de características: {e}")
        return []
    