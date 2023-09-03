import re

def limpiar_cadena(cadena):
    # Eliminar espacios iniciales y finales
    # cadena = cadena.strip()

    # # Utilizar una expresión regular para eliminar números, guiones y porcentaje dentro del paréntesis
    # patron = r'\(\d+\.\d+%?\)'
    # cadena = re.sub(patron, '', cadena)

    # Luego eliminar cualquier otro carácter que no sea una letra o un espacio
    cadena = re.sub(r'[^a-zA-Z\s]', '', cadena).strip()

    return cadena