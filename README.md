# Descripción del Proyecto

Este proyecto es una función Lambda en Python 3.10 con una arquitectura x86_64, que interactúa con una API externa para obtener y procesar información sobre personajes. La función permite buscar personajes por nombre o ID, así como realizar una consulta general para obtener todos los personajes. Utiliza la biblioteca `requests` para las solicitudes HTTP y maneja errores y registros mediante el módulo `logging`.

## Funcionalidades Principales

1. **Buscar personajes**: La función `buscar_personajes` realiza una solicitud GET a un endpoint `/character` de la API externa configurada en la variable de entorno `API_URL`. Devuelve los datos en formato JSON si la solicitud es exitosa; de lo contrario, registra y lanza un error.

2. **Buscar personaje por nombre**: La función `buscar_personaje_nombre` permite buscar un personaje específico utilizando el nombre proporcionado en la consulta. Realiza una solicitud GET al endpoint `/character/?name={nombre}` y devuelve los datos en formato JSON.

3. **Buscar personaje por ID**: La función `buscar_personaje_id` permite buscar un personaje específico usando su ID. Realiza una solicitud GET al endpoint `/character/{id}` y devuelve los datos en formato JSON.

4. **Procesar personajes**: La función `procesar_personajes` extrae y formatea la información relevante de los personajes obtenidos. Si algunos datos están ausentes, asigna valores por defecto como "Unknown".

5. **lambda_handler**: La función principal `lambda_handler` orquesta las llamadas para obtener y procesar los personajes en función de los parámetros de la solicitud entrante. Puede buscar personajes por nombre, ID, o devolver todos los personajes si no se especifican parámetros. Maneja los errores y devuelve una respuesta adecuada con el código HTTP correspondiente.

## Manejo de Errores

El código incluye manejo de excepciones para errores durante las solicitudes HTTP y el procesamiento de datos. En caso de error, se registra un mensaje detallado y se retorna una respuesta con código HTTP 500, que incluye información sobre la consulta y ruta que causaron el error.

## Configuración de la Capa para la Biblioteca `requests`

Se adjunta la carpeta.zip necesaria para utilizar la biblioteca `requests` en un entorno AWS Lambda, por medio de la creación de una capa, esto garantizará que la función Lambda pueda realizar solicitudes HTTP correctamente.

## Variables de Entorno

- **API_URL**: El valor de esta variable fue colocada en las variables de entorno de AWS Lambda. Esta URL corresponde a la API externa desde donde se obtendrán los personajes de Rick and Morty

## Registro de Logs

El código utiliza el módulo `logging` de Python para registrar eventos importantes, como errores durante las solicitudes HTTP o durante el procesamiento de los datos.

## Respuesta de la API

- **Código 200**: Si la solicitud y el procesamiento de datos son exitosos.
- **Código 500**: En caso de errores, se proporciona un mensaje de error y detalles de la consulta.
