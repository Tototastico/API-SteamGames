# Proyecto MLOps en Steam

![Steam Logo](inserta_el_enlace_de_la_imagen_del_logo_de_Steam)

Este proyecto se enfoca en la creación de un sistema de recomendación de videojuegos para usuarios de Steam, la plataforma multinacional de videojuegos. Como MLOps Engineer, hemos trabajado desde cero para convertir datos crudos en un sistema de recomendación funcional. Este README proporciona una visión general de mi trabajo y cómo implementar y utilizar la API resultante.

## Contenido del README

- [Descripción del Problema](#descripción-del-problema)
- [Requerimientos de Aprobación](#requerimientos-de-aprobación)
- [Exploratory Data Analysis (EDA)](#exploratory-data-analysis-eda)
- [Modelo de Aprendizaje Automático](#modelo-de-aprendizaje-automático)
- [Implementación de la API](#implementación-de-la-api)
- [Cómo Usar la API](#cómo-usar-la-api)
- [Video de Demostración](#video-de-demostración)
- [Repositorio](#repositorio)
- [Fuentes de Datos](#fuentes-de-datos)

## Descripción del Problema

Steam necesitaba un sistema de recomendación de videojuegos para sus usuarios. Los datos iniciales eran desafiantes, con datos crudos y falta de automatización en la actualización de nuevos productos. Como MLOps Engineer, tuvimos que realizar tareas de Data Engineering y crear un MVP para abordar este problema.

## Requerimientos de Aprobación

### Transformaciones

- Se ha realizado la lectura del dataset en el formato correcto.
- Las columnas innecesarias se han eliminado para optimizar el rendimiento de la API y el entrenamiento del modelo.

### Feature Engineering

- Se ha creado la columna 'sentiment_analysis' aplicando análisis de sentimiento con NLP.
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

- Se ha implementado el despliegue de la API, utilizando el rervicio de Render.

### Análisis Exploratorio de Datos (EDA)

- Se ha realizado un análisis exploratorio de datos para comprender las relaciones y patrones en el dataset.

### Modelo de Aprendizaje Automático

Hemos implementado un sistema de recomendación de videojuegos utilizando el enfoque de [elegir uno de los dos]:

- **Ítem-Ítem**: Este sistema recomienda juegos similares a un juego dado.
- **User-Ítem**: Este sistema recomienda juegos a un usuario basado en usuarios similares.

## Exploratory Data Analysis (EDA)

Se ha realizado un análisis exploratorio de datos para comprender mejor el dataset, incluyendo:

- Identificación de relaciones entre variables.
- Identificación de outliers o anomalías.
- Exploración de patrones interesantes.

## Modelo de Aprendizaje Automático

Hemos implementado un sistema de recomendación de videojuegos utilizando el enfoque de [elegir uno de los dos]:

- **Ítem-Ítem**: Este sistema recomienda juegos similares a un juego dado.
- **User-Ítem**: Este sistema recomienda juegos a un usuario basado en usuarios similares.

## Implementación de la API

La API se ha implementado utilizando el framework FastAPI y proporciona los siguientes endpoints:

- `/userdata(User_id: str)`
- `/countreviews(YYYY-MM-DD y YYYY-MM-DD: str)`
- `/genre(género: str)`
- `/userforgenre(género: str)`
- `/developer(desarrollador: str)`
- `/sentiment_analysis(año: int)`

## Cómo Usar la API

[Instrucciones sobre cómo utilizar la API y ejemplos de consultas]

## Video de Demostración

Puedes ver una demostración de la API y el modelo de recomendación en funcionamiento en el siguiente enlace: [Enlace al Video](inserta_el_enlace_del_video_de_demostración)

## Repositorio

El código fuente de este proyecto se encuentra en el siguiente repositorio: [Enlace al Repositorio](inserta_el_enlace_del_repositorio)

## Fuentes de Datos

- Dataset: [Enlace al Dataset](inserta_el_enlace_del_dataset)
- Diccionario de Datos: [Enlace al Diccionario de Datos](inserta_el_enlace_del_diccionario_de_datos)
