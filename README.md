# Descripción del Proyecto

Este proyecto es una función Lambda en Python 3.10 con arquitectura x86_64, que realiza consultas a una API externa para obtener información sobre personajes y procesar los datos relevantes. Utiliza la biblioteca `requests` para realizar las consultas HTTP y devuelve los resultados en formato JSON. El código se puede desplegar como una función Lambda en AWS.

## Funcionalidades Principales

1. **Buscar personajes**: La función `buscar_personajes` realiza una solicitud GET a un endpoint `/character` de la API externa configurada en la variable de entorno `API_URL`. Si la solicitud es exitosa, devuelve los datos en formato JSON; de lo contrario, registra y lanza un error.

2. **Procesar personajes**: La función `procesar_personajes` toma los datos obtenidos y los filtra para extraer información clave sobre cada personaje, como el nombre, estado, especie, origen, ubicación, imagen y otros detalles. Si faltan ciertos datos, se les asigna un valor por defecto como "Unknown".

3. **Manejo de errores**: El código incluye manejo de excepciones tanto para errores en la solicitud HTTP como para posibles problemas al procesar los datos, con mensajes de error detallados que se registran para facilitar el debugging.

4. **lambda_handler**: Esta es la función principal que ejecuta la lógica del Lambda, orquestando las llamadas para obtener y procesar los personajes. Retorna una respuesta con código HTTP 200 si todo fue correcto, o un código 500 en caso de error.

## Configuración de la Capa para la Biblioteca `requests`

Para poder utilizar la biblioteca `requests` en un entorno AWS Lambda, se adjunta un archivo ZIP que contiene los archivos necesarios para crear una capa (`Layer`) que puede ser añadida a la función Lambda. Esta capa incluye las dependencias requeridas, asegurando que el código pueda realizar solicitudes HTTP correctamente.

## Variables de Entorno

- **API_URL**: Debe ser configurada en las variables de entorno de AWS Lambda. Esta URL corresponde a la API externa desde donde se obtendrán los personajes de Rick and Morty

## Registro de Logs

El código utiliza el módulo `logging` de Python para registrar eventos importantes, como errores durante las solicitudes HTTP o durante el procesamiento de los datos.
