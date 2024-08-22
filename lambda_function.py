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
    
    # Realizar consulta
    try:
        response = requests.get(url)
        response.raise_for_status()
        #Retornar respuesta
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f' Ha ocurrido un error al realizar la consula: {e}')
        raise 

# Procesar personajes:
def procesar_personajes(datos):
    
    datos_obtenidos = datos.get('results')
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
                'error': 'Internal Server Error'
            }),
            'headers': {
                'Content-Type': 'application/json'
            }
        }
