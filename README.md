# Mi Proyecto: Sistema de Recomendación de Videojuegos para Steam

![](https://github.com/Hotcer/Steam_FastAPI/blob/master/imagenes/1.jpg)
Este es mi README para un proyecto que he realizado con el objetivo de crear un sistema de recomendación basado en machine learning para Steam, una plataforma multinacional de videojuegos. Como científico de datos en Steam, mi rol fue desarrollar un sistema que recomendara videojuegos a los usuarios. El proyecto abarcó diversas etapas, incluyendo ingeniería de datos, desarrollo de API, análisis exploratorio de datos (EDA) y creación de modelos de machine learning.

## Descripción del Problema

En el contexto de este proyecto, me enfoqué en la creación de un sistema de recomendación de videojuegos para Steam. Los datos del proyecto se encontraban en un estado crudo e inmaduro, lo que hizo que la ingeniería de datos fuera esencial para prepararlos para el análisis y la modelización. Mi objetivo fue crear un Producto Mínimo Viable (MVP) que abordara este problema y entregara un sistema de recomendación funcional.

## Trabajo Realizado

### Transformación de Datos

Para el MVP, me centré en preparar el conjunto de datos en el formato correcto. Eliminé columnas innecesarias para optimizar el rendimiento de la API y el entrenamiento del modelo. Además, realicé transformaciones de datos cuando fue necesario para mejorar la calidad de los datos.

### Ingeniería de Características

Creé una nueva columna llamada 'sentiment_analysis' en el conjunto de datos 'user_reviews' utilizando análisis de sentimiento mediante Procesamiento de Lenguaje Natural (NLP). Asigné valores '0' para opiniones negativas, '1' para opiniones neutrales y '2' para opiniones positivas. Esta columna reemplazó la columna 'user_reviews.review' para facilitar el entrenamiento del modelo de machine learning y el análisis de datos. Cuando faltaban opiniones, establecí el valor de 'sentiment_analysis' en 1.

### Desarrollo de la API

Desarrollé una API utilizando el framework FastAPI para proporcionar acceso a los datos de Steam. Puedes acceder a la [API aquí](https://steamgames-fastapi.onrender.com/docs#/).


1. `PlayTimeGenre(género: str)`: Devuelve el año con más horas jugadas para el género dado.

   Ejemplo de retorno: `{"Año con más horas jugadas para Género X" : 2013}`

2. `UserForGenre(género: str)`: Devuelve el usuario con las horas acumuladas más altas jugadas para el género dado y una lista de horas acumuladas jugadas por año.

   Ejemplo de retorno: `{"Usuario con más horas jugadas para Género X" : us213ndjss09sdf, "Horas jugadas":[{Año: 2013, Horas: 203}, {Año: 2012, Horas: 100}, {Año: 2011, Horas: 23}]}`

3. `UsersRecommend(año: int)`: Devuelve los 3 juegos más recomendados por los usuarios para el año dado. (reseñas.recomendar = True y comentarios positivos/neutrales)

   Ejemplo de retorno: `[{"Puesto 1" : X}, {"Puesto 2" : Y},{"Puesto 3" : Z}]`

4. `UsersNotRecommend(año: int)`: Devuelve los 3 juegos menos recomendados por los usuarios para el año dado. (reseñas.recomendar = False y comentarios negativos)

   Ejemplo de retorno: `[{"Puesto 1" : X}, {"Puesto 2" : Y},{"Puesto 3" : Z}]`

5. `sentiment_analysis(año: int)`: Devuelve una lista del número de registros de reseñas de usuarios categorizados por análisis de sentimiento para el año especificado.

   Ejemplo de retorno: `{"Negativo": 182, "Neutral": 120, "Positivo": 278}`

### Implementación

Implementé la API utilizando la plataforma de Render, asegurándome de que fuera accesible desde internet.

## Análisis Exploratorio de Datos (EDA)

Conduje un análisis exploratorio de datos para investigar las relaciones entre las variables del conjunto de datos, identificar valores atípicos o anomalías y descubrir patrones interesantes. Generé nubes de palabras para visualizar las palabras más frecuentes en los títulos de los juegos, lo cual podría ser útil para el sistema de predicción.

## Modelo de Machine Learning
![](https://github.com/Hotcer/Steam_FastAPI/blob/master/imagenes/3.jpg?raw=true)
Después de limpiar y hacer que los datos fueran consumibles a través de la API, entrené un modelo de machine learning para construir un sistema de recomendación. Opté por desarrollar un Sistema de Recomendación de Usuarios-Ítems que recomienda juegos a un usuario en función de las preferencias de usuarios similares.

El punto final de la API para esta funcionalidad es `recomendacion_usuario(id del usuario)`.

## Notas Importantes

- Aseguré que el MVP fuera una API RESTful que se pudiera acceder desde cualquier dispositivo conectado a internet.
- Utilicé la herramienta FastAPI para el desarrollo de la API.
- Implementé la API en la plataforma Render.
- Realicé análisis exploratorios de datos de forma manual para obtener una comprensión más profunda de los datos.

Concluí el proyecto siguiendo estas pautas y completando las tareas propuestas, contribuyendo así al desarrollo de un potente sistema de recomendación para la plataforma de videojuegos de Steam. ¡Fue un proyecto emocionante y enriquecedor!

[![agaradecimeintos.jpg](https://i.postimg.cc/65y6W3jk/agaradecimeintos.jpg)](https://postimg.cc/HV113pCz)
