#Pixeles extra a sumar a los calculos de la imágen para que no quede tan justa
margen_error = 70 

def recortar(imagen, centro_circulo, radio):
    """
    Recorta la imagen recibida.

    A partir del centro del circulo de la imagen recibida y el radio del mismo,
    calcula los valores necesarios para recortar la imágen y solo quedarse con 
    el rectangulo que encierra a dicho circulo.

    Parametros:
        imagen (Image): La imagen a recortar.
        centro_circulo (tuple): Tuple con el valor (x,y) el centro del circulo.
        radio (int): Radio del circulo de la imágen

    Regreso:
        Image: La imágen recortada a solo el rectangulo que encierra el circulo.
    """
    izquierda = centro_circulo[0] - radio - margen_error
    arriba = centro_circulo[1] - radio - margen_error
    derecha = centro_circulo[0] + radio + margen_error
    abajo = centro_circulo[1] + radio + margen_error

    imagen = imagen.crop((izquierda, arriba, derecha, abajo))
    return imagen

def calcular_nuevo_ancho_imagen(radio):
    """Calcula el nuevo ancho de la imagen recortada."""
    return (radio + margen_error)*2

def calcular_nuevo_largo_imagen(radio):
    """Calcula el nuevo largo de la imagen recortada."""
    return (radio + margen_error)*2

def calcular_nuevo_centro_circulo(radio):
    """Calcula el nuevo centro del circulo de la imágen recortada"""
    centro = (radio + margen_error)
    return (centro, centro)


