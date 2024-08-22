import json
import request 
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
        response = request.get(url)
        response.raise_for_status()
        #Retornar respuesta
        return response.json()
    except request.exceptions.RequestException as e:
        logger.error(f' Ha ocurrido un error al realizar la consula: {e}')
        raise 
