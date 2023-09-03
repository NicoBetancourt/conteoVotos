import re

def limpiar_cadena(cadena):

    # Se eliminan espacios y caracteres especiales
    cadena = re.sub(r'[^a-zA-Z\s]', '', cadena).strip()

    return cadena