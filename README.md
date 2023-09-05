# Proyecto MLOps en Steam

Este proyecto se enfoca en la creación de un sistema de recomendación de videojuegos para usuarios de Steam, la plataforma multinacional de videojuegos. Como MLOps Engineer, hemos trabajado desde cero para convertir datos crudos en un sistema de recomendación funcional. Este README proporciona una visión general de mi trabajo y cómo implementar y utilizar la API resultante.

## Contenido del README

- [Descripción del Problema](#descripción-del-problema)
- [Exploratory Data Analysis (EDA)](#exploratory-data-analysis-(EDA))
- [Modelo de Aprendizaje Automático](#modelo-de-aprendizaje-automático)
- [Implementación de la API](#implementación-de-la-api)
- [Cómo Usar la API](#cómo-usar-la-api)
- [Video de Demostración](#video-de-demostración)
- [Repositorio](#repositorio)
- [Fuentes de Datos](#fuentes-de-datos)

## Descripción del Problema

Steam necesitaba un sistema de recomendación de videojuegos para sus usuarios. Los datos iniciales eran desafiantes, con datos crudos y poco limpios. Como MLOps Engineer, tuve que realizar tareas de Data Engineering y crear un MVP para abordar este problema, ademas de otras funciones.

### Transformaciones

- Se ha realizado la lectura de los datasets en el formato JSON.
- Se ha realizado una exhaustiva transformacion de datos, limpieza, imputacion de datos faltantes
mapeo de emojis, etc.
- Y se han exportado como .parquet comprimidos con GZIP
- Las columnas y filas innecesarias se han eliminado para optimizar el rendimiento de la API y el entrenamiento del modelo.

### Feature Engineering

- Se ha creado la columna 'sentiment_analysis' aplicando análisis de sentimiento con NLP, (NLTK)
- La columna 'sentiment_analysis' reemplaza la columna 'user_reviews.review' según lo especificado.

### Desarrollo de la API

- Se han creado las siguientes funciones para los endpoints de la API:
  - `userdata(User_id: str)`
  - `countreviews(YYYY-MM-DD y YYYY-MM-DD: str)`
  - `genre(género: str)`
  - `userforgenre(género: str)`
  - `developer(desarrollador: str)`
  - `sentiment_analysis(año: int)`

### Deployment

- Implemente el despliegue de la API, utilizando el rervicio de Render.
- Puedes utilizar la api desde aqui: [Enlace a la API](https://mlops-deploy-lngj.onrender.com)

### Modelo de Aprendizaje Automático

Tambien implemente un sistema de recomendación de videojuegos utilizando el enfoque de Item-Item:

- **Ítem-Ítem**: Este sistema recomienda juegos similares a un juego dado.

## Exploratory Data Analysis (EDA)

Se ha realizado un análisis exploratorio de datos para comprender mejor el dataset, incluyendo:

- Identificación de relaciones entre variables.
- Identificación de outliers o anomalías.
- Exploración de patrones interesantes.
- Analisis de datos a traves del tiempo.

## Cómo Usar la API

Para poder utilizar la API debemos acceder a este vinculo: [Enlace de la API](https://mlops-deploy-lngj.onrender.com)
Luego podremos acceder a cada funcion desde el hipervinculo, funcion por funcion, de esta manera:

  - `userdata(User_id: str)` https://mlops-deploy-lngj.onrender.com/userdata/{User_id}
  - `countreviews(YYYY-MM-DD y YYYY-MM-DD: str)` https://mlops-deploy-lngj.onrender.com/countreviews/{Fecha_inicio,Fecha_final}
  - `genre(género: str)` https://mlops-deploy-lngj.onrender.com/genre/{Genero}
  - `userforgenre(género: str)` https://mlops-deploy-lngj.onrender.com/userforgenre/{Genero}
  - `developer(desarrollador: str)` https://mlops-deploy-lngj.onrender.com/developer/{Empresa}
  - `sentiment_analysis(año: int)` https://mlops-deploy-lngj.onrender.com/sentiment_analysis/{Año}

Cada funcion con su respectivo link, cabe aclarar que los corchetes no van, es para demostrar que ahi hay que insertar una variable, y en la funcion de countreviews, los parametros van separados con una ","

[Enlace a la documentacion](https://mlops-deploy-lngj.onrender.com/docs) Aqui podremos acceder a una interfaz visual para trabajar nuestra API

## Video de Demostración

Puedes ver una demostración de la API y el modelo de recomendación en funcionamiento en el siguiente enlace: [Enlace al Video](https://www.youtube.com/watch?v=weGiBijRPdE)

## Repositorio

El código fuente de este proyecto se encuentra en el siguiente repositorio: [Enlace al Repositorio](https://github.com/Tototastico/ML-OPS)

## Fuentes de Datos

- Datasets: [Enlace al Dataset](https://drive.google.com/drive/folders/1HqBG2-sUkz_R3h1dZU5F2uAzpRn7BSpj)

## Aclaraciones

Este trabajo esta realizado con una reduccion de datasets, tal vez es una decision incorrecta a la hora de hacer modelos y/o funciones precisas, pero he tenido que desarrollarlo de esta manera, por dos razones, 1: que mi computadora no superaba la RAM necesaria para crear el coseno de similaridad, y 2: que Render, no permitia correr algunas funciones, incluido el modelo, porque superaba las 512Mb de RAM. Si ambas opciones se solucionarian, podria costruir una API precisa y un modelo mas preciso.

Developed by:
## Tobias Ezequiel Sirne
