import sys
from PIL import Image

class ErrorFormato(Exception):
    """Excepción para manejar errores de formato de imagen."""
    pass

class ErrorDimension(Exception):
    """Excepción para manejar errores de dimensiones de imagen."""
    pass

def verificar_imagen(nombre_imagen, ancho_imagen, largo_imagen):
    """
    Verifica si una imagen cumple con el formato y dimensiones especificados.

    Parametros:
    - nombre_imagen (str): El nombre del archivo de la imagen.
    - ancho_imagen (int): El ancho deseado de la imagen.
    - largo_imagen (int): El largo deseado de la imagen.

    Regresa:
    - bool: True si la imagen cumple con los requisitos, False en caso contrario.
    """
    try:
        img = Image.open(nombre_imagen)
        
        # Verificar que la imagen está en formato JPEG
        if img.format != 'JPEG':
            raise ErrorFormato(f"La imagen {nombre_imagen} no está en formato JPEG.")
        
        # Verificar que la imagen tiene las dimensiones correctas
        if img.size != (ancho_imagen, largo_imagen):
            raise ErrorDimension(f"La imagen {nombre_imagen} no tiene las dimensiones correctas. Debe ser de {ancho_imagen} px de ancho y {largo_imagen} px de alto.")
    except IOError:
        print(f"No se pudo abrir la imagen {nombre_imagen}.")
        return False

def manejar_entrada():
    """
    Maneja los argumentos de la línea de comandos.

    Regresa:
    - tuple: Una tupla con el nombre de la imagen y un indicador booleano ('S').
             (None, False) si no se proporciona el nombre de la imagen.
    """
    # Verificar que se proporcionó el nombre de la imagen
    if len(sys.argv) < 2:
        print("Por favor, proporciona el nombre de una imagen.")
        return None, False

    nombre_imagen = sys.argv[1]
    
    # Verificar si se proporcionó la bandera 'S'
    bandera_s = len(sys.argv) > 2 and sys.argv[2].lower() == 's'
    
    return nombre_imagen, bandera_s