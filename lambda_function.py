import json
import requests
import logging
import os
 
# Configurar logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Configurar el URL 
API_URL = os.getenv('API_URL')

# Buscar personajes 
def buscar_personajes():
    # Agregar sufijo a la url almacenada
    url = API_URL + '/character'
    
    #Lista para almacenar personajes
    todos_los_personajes = []
    contador = 0
    while url:
        try:
            # Realizar la consulta a la API
            response = requests.get(url)
            response.raise_for_status()

            # Convertir la respuesta en JSON
            datos = response.json()

            # Agregar los personajes de la página actual a la lista
            todos_los_personajes.extend(datos['results'])

            # Actualizar la URL con la URL de la siguiente página (si existe)
            # Actualizar la URL con la URL de la siguiente página (si existe)
            next_url = datos['info'].get('next')
            contador = contador + 1
            print(contador)
            print(next_url)
            if next_url is None:
                print('No more pages.')
                break
            else:
                url = next_url

        except requests.exceptions.RequestException as e:
            logger.error(f'Ha ocurrido un error al realizar la consulta: {e}')
            raise
        
    print(f'Total de personajes obtenidos: {len(todos_los_personajes)}')
    # Retornar todos los personajes obtenidos
    return todos_los_personajes
    
# Buscar un personaje por nombre en especifico
def buscar_personaje_nombre(nombre):
    # Preparar la ruta completa con el nombre a buscar
    url = API_URL + f'/character/?name={nombre}'
    
    #Realizar consulta
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f'Error al realizar la consulta: {e}')
        raise
    
# Buscar un personaje por id en especifico
def buscar_personaje_id(id):
    # Preparar la ruta completa con el id a buscar
    url = API_URL + f'/character/{id}'
    
    #Realizar consulta
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f'Error al realizar la consulta: {e}')
        raise

# Procesar personajes:
def procesar_personajes(datos):
    #Preparar los datos obtenidos, así como un objeto único, en un array iterable
    try:
        datos_obtenidos = datos.get('results', [datos])
    except:
        datos_obtenidos = datos
    # Extrae los datos más relevantes de los personajes
    try: 
        # Procesa los datos de los personajes, si no hay información disponible
        # retorna un valor "desconocido"
        personajes = [{
            'name': personaje.get('name', 'Unknown name'),
            'status': personaje.get('status', 'Unknown status'),
            'species': personaje.get('species', 'Unknown specie'),
            'type': personaje.get('type', 'Unknown type'),
            'gender': personaje.get('gender', 'Unknown gender'),
            'origin': {
                'name': personaje.get('origin', {}).get('name', 'Unknown Origin name'),
                'url': personaje.get('origin', {}).get('url', 'Unknown URL')
            },
            'location': {
                'name': personaje.get('location', {}).get('name', 'Unknown location name'),
                'url': personaje.get('location', {}).get('url', 'Unknown URL')
            },
            'image': personaje.get('image', 'Unknown image'),
            'url': personaje.get('url', 'Unknown url'),
            'created': personaje.get('created', 'Unknown created')
        } for personaje in datos_obtenidos]
        # Retornar información
        return personajes
    except KeyError as e:
        logger.error(f"Error al procesar los datos: {e}")
        print(logger.error(f"Error al procesar los datos: {e}"))
        raise

def lambda_handler(event, context):
    # Función principal 
    try:
        
        #Obtener los parámetros de la solicitud entrante
        parametros_ruta = event.get('pathParameters', {})
        parametros_query = event.get('queryStringParameters', {})
        print(parametros_query, 23)

         # Determinar qué búsqueda realizar
        if 'name' in parametros_query:
            nombre = parametros_query['name']
            datos = buscar_personaje_nombre(nombre)
        elif 'id' in parametros_query:
            id = parametros_query['id']
            datos = buscar_personaje_id(id)
        else:
            # Obtener datos de la Api a través del método
            datos = buscar_personajes()
        
        #Procesar los datos obtenidos
        personajes = procesar_personajes(datos)
        
        # Retornar los datos 
        return {
            'statusCode': 200,
            'body': personajes,
            'mensaje': 'Se ha obtenido correctamente la información',
            'headers': {
                'Content-Type': 'application/json'
            }
        }
    except Exception as e:
        #Procesar error general 
        return {
            'statusCode': 500,
            'body': json.dumps({
                'mensaje': 'Error al obtener los datos',
                'error': 'Internal Server Error',
                'query': parametros_query,
                'ruta': parametros_ruta
            }),
            'headers': {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": 'GET, POST, PUT, DELETE, OPTIONS',
            'Content-Type': 'application/json'
            }
        }
