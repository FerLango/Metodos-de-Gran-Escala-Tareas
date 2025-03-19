# Tarea 06

En el capítulo anterior aprendiste a construir un ETL y un ELT para 
extraer datos de una fuente y llevarlos a un destino con alguna transformación.
Esto con la finalidad de almacenar datos para luego analizarlos o aplicarles
un modelo estadístico o de machine learning.

En esta tarea vas a poner en práctica lo que haz aprendido sobre ETLs, Amazon S3,
Amazon Athena y AWS Glue Catalog.

## Objetivo

1. Implementa la siguiente arquitectura para analizar la relación entre el 
tipo de cambio PESO/USD, la tasa de interés y la inflación. Estos datos 
provienen del Banco de México y el INEGI.

![Arquitectura](tareas/arquitectura05.png)

1.1 Construye un ETL para descargar los datos del Banco de México y el INEGI y
almacenalos en Amazon S3. En una carpeta dentro de tu bucket `itam-analytics-NOMBRE` 
dentro de un folder que se llame `raw`. Antes de subir los archivos tendras
que limpiar la tabla utilizando pandas, de tal forma que te quede una tabla 
que puedas con el `timestamp` y la `nombre_serie de tiempo`. Debes tener
un archivo por cada serie de tiempo.

- `tipo_de_cambio.csv`
- `tasa_de_interes.csv`
- `inflacion.csv`


1.2 Construye una base de datos en Amazon Glue, que se llame `econ`. Para crearla
entra a la consola de AWS en el servicio de Glue, luego en databases.

1. Construye un ELT para que puedas construir una tabla con tres columnas con
frecuencia mensual:

- `date` (YYYY-MM-DD)
- `tasa_de_interes`,
- `inflacion`

2.1 Con Amazon Athena y un Notebook de Python, crea tres tablas, una que se 
llamen:

- `tipo_de_cambio`,
- `tasa_de_interes`,
- `inflacion`

Nota: Puedes utilizar la consola de Amazon Athena, para crear dentro de la 
base de datos `econ`, los DDL (el código de SQL para crear la tabla). Este 
código los puedes pegar en tu notebook, para que este código pueda correr de
manera automatizada. No querras repetir cada semana esta carga de datos 
manualmente en la consola.

2.2 Crea en tu notebook una Query con SQL para correr en Athena, que te
permita hacer un join de las tres tablas, para derivar el schema del punto 2.

3 Desde una nuevo notebook de Python, conectate a Athena, para descargar
en un dataframe la tabla que creaste con el ELT.

3.1 Crear tres regresiones lineales:

- `tipo_de_cambio ~ tasa_de_interes`
- `tasa_de_interes ~ inflacion`
- `tipo_de_cambio  ~ inflacion`

3.2 Gráfica un scatter plot para estas tres regresiones y añade el fit de las
regresiones.

4. Para visualizar tus resultados, utiliza una aplicación de streamlit. Hay
   muchas maneras de hacerlo. Usa tu creatividad. Si no recuerdas como comenzar
   con streamlit usa el link de este tutorial. [Create an app](https://docs.streamlit.io/get-started/tutorials/create-an-app).

## Implementación

- Conectate a las APIs del Banco de México y el INEGI para descargar los 
datos. Estas conexiones deberán de ir en tu script, utiliza un `config.ini` o un
`config.yaml` para guardar los tokens de las APIs.

- Para el Banco de México, puedes utilizar el siguiente paquete:

    * https://pypi.org/project/sie-banxico/

- Para el INEGI, puedes utilizar el siguiente paquete:

    * https://pypi.org/project/INEGIpy/ 


## TIP

- Piensa en las temproalidades de la series.

## Entregables:

* script ETLs
* script ELTs
* Notebook Analytics con las regresiones y las visualizaciones
* App de Streamlit


