# Proyecto de Predicción de Precios de Casas

## Descripción

Este proyecto tiene como objetivo predecir los precios de venta de casas utilizando un conjunto de datos de precios de compra-venta de casas de la ciudad Ames, Iowa en Estados Unidos. El proyecto incluye scripts para preprocesamiento de datos, entrenamiento de modelos y generación de predicciones.

## Estructura del Repositorio

```plaintext
├── README.md
├── data
│   ├── inference
│   │   └── test.csv
│   ├── predictions
│   │   └── predictions.csv
│   ├── prep
│   │   └── train_clean.csv
│   └── raw
│       ├── data_description.txt
│       ├── sample_submission.csv
│       └── train.csv
├── model
│   └── model.joblib
├── notebooks
│   └── Tarea 03.ipynb
├── src
│   ├── __pycache__
│   │   ├── inference.cpython-311.pyc
│   │   ├── prep.cpython-311.pyc
│   │   ├── train.cpython-311.pyc
│   │   └── utils.cpython-311.pyc
│   ├── inference.py
│   ├── prep.py
│   ├── train.py
│   └── utils.py
└── tarea03.md
```

## Scripts

### `src/prep.py`

Este script contiene la función `prepare_data` que preprocesa los datos de entrada y guarda los datos procesados.

### `src/train.py`

Este script contiene la función `train_model` que entrena un modelo utilizando los datos de entrada y guarda el modelo entrenado.

### `src/inference.py`

Este script contiene la función `make_inference` que realiza predicciones sobre los datos de entrada usando un modelo entrenado y guarda las predicciones en un archivo CSV.

### `src/utils.py`

Este script contiene funciones de utilidad para la limpieza de datos y la selección de características.

## Notebooks

### `notebooks/Tarea 03.ipynb`

Este notebook contiene el análisis exploratorio de datos, la experimentación con diferentes modelos y la evaluación de los resultados.

## Datos

### `data/raw/`

Contiene los datos crudos sin procesar.

### `data/prep/`

Contiene los datos preprocesados listos para el entrenamiento del modelo.

### `data/inference/`

Contiene los datos de entrada para realizar inferencias.

### `data/predictions/`

Contiene las predicciones generadas por el modelo.

## Modelo

### `model/model.joblib`

Archivo que contiene el modelo entrenado.

## Ejecución

### Preprocesamiento de Datos

```bash
python src/prep.py
```

### Entrenamiento del Modelo

```bash
docker build -f docker/train/Dockerfile -t entrenamiento_casas .
docker run --rm -v "$(pwd)/data":/app/data -v "$(pwd)/model":/app/model entrenamiento_casas --input_path data/prep/train_clean.csv --model_output_path model/model.joblib
```

### Inferencia

```bash
docker build -f docker/inference/Dockerfile -t inferencia_casas .
docker run --rm -v "$(pwd)/data":/app/data -v "$(pwd)/model":/app/model inferencia_casas --input_path data/inference/test.csv --model_path model/model.joblib --output_path data/predictions/predictions.csv
```










