import streamlit as st
import awswrangler as wr
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import date

# Parámetros de conexión a Athena
DATABASE = "econ"
ATHENA_OUTPUT = "s3://itam-analytics-ferlango/athena_results/"
QUERY = "SELECT * FROM mensual"

st.title("Análisis Económico: Regresiones y Visualización")

# Cache de datos con la nueva función de Streamlit (st.cache_data)
@st.cache_data(show_spinner=True)
def load_data():
    df = wr.athena.read_sql_query(sql=QUERY, database=DATABASE, s3_output=ATHENA_OUTPUT)
    # Convertir 'date' a tipo datetime y luego extraer solo la fecha (sin hora)
    df['date'] = pd.to_datetime(df['date']).dt.date  
    return df

df = load_data()

st.subheader("Datos Consolidados")
total_registros = df.shape[0]
st.write(f"Se encontraron {total_registros} registros en total.")

# Slider para seleccionar el rango de fechas
min_date = df['date'].min()
max_date = df['date'].max()

date_range = st.slider(
    "Selecciona el periodo de tiempo:",
    min_value=min_date,
    max_value=max_date,
    value=(min_date, max_date),
    format="YYYY-MM-DD"
)

# Filtrar el DataFrame según el rango seleccionado
filtered_df = df[(df['date'] >= date_range[0]) & (df['date'] <= date_range[1])]

st.write(f"Mostrando {filtered_df.shape[0]} de {df.shape[0]} registros filtrados.")
st.dataframe(filtered_df, height=300)

# Función para realizar la regresión y graficar el scatter plot con línea de ajuste
def plot_regression(x, y, xlabel, ylabel, title):
    slope, intercept = np.polyfit(x, y, 1)
    line = slope * x + intercept
    fig, ax = plt.subplots(figsize=(8,6))
    ax.scatter(x, y, color='blue', alpha=0.7, label="Datos")
    ax.plot(x, line, color='red', linewidth=2, label=f"Fit: y = {slope:.2f}x + {intercept:.2f}")
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.legend()
    ax.grid(True)
    return fig

# Actualizar los gráficos usando los datos filtrados

st.header("Regresión: Tipo de Cambio ~ Tasa de Interés")
if not filtered_df.empty:
    fig1 = plot_regression(
        x=filtered_df['tasa_de_interes'],
        y=filtered_df['tipo_de_cambio'],
        xlabel="Tasa de Interés",
        ylabel="Tipo de Cambio",
        title="Tipo de Cambio vs Tasa de Interés"
    )
    st.pyplot(fig1)
else:
    st.write("No hay datos para el rango seleccionado.")

st.header("Regresión: Tasa de Interés ~ Inflación")
if not filtered_df.empty:
    fig2 = plot_regression(
        x=filtered_df['inflacion'],
        y=filtered_df['tasa_de_interes'],
        xlabel="Inflación",
        ylabel="Tasa de Interés",
        title="Tasa de Interés vs Inflación"
    )
    st.pyplot(fig2)
else:
    st.write("No hay datos para el rango seleccionado.")

st.header("Regresión: Tipo de Cambio ~ Inflación")
if not filtered_df.empty:
    fig3 = plot_regression(
        x=filtered_df['inflacion'],
        y=filtered_df['tipo_de_cambio'],
        xlabel="Inflación",
        ylabel="Tipo de Cambio",
        title="Tipo de Cambio vs Inflación"
    )
    st.pyplot(fig3)
else:
    st.write("No hay datos para el rango seleccionado.")
