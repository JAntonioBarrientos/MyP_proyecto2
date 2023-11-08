from PIL import Image, ImageDraw
import numpy as np

def procesa_imagen_a_blanco_y_negro(imagen):
    """
    Mediante una imagen del cielo crea otra donde los pixeles blancos sean nubes y los negros cielo.

    Recibe una imagen que será trabajada en RGB y para cada pixel de esta, se calcula el cociente R/B
    (el valor rojo del pixel entre el valor azul del pixel), y mediante un umbral (0.95) definido en el artículo 
    (Roy, G., S. Hayman y W. Julian, "Sky analysis from CCD images: cloud cover", Lighting
    Research Technology, Vol. 33, No. 4, pp. 211-222, 2001) se determina si clasificar al pixel como 
    nube o como cielo.

    Parametros:
        imagen (Image): La imagen a procesar

    Regreso
        Image: La imagen ya procesada en blanco y negro
    """

    imagen = imagen.convert("RGB")
    imagen_arreglo = np.asarray(imagen)
    imagen_BN = ImageDraw.Draw(imagen)
    umbral = 0.95
    it = np.nditer(imagen_arreglo[:, :, 0], flags=["multi_index"])

    while not it.finished:
        x, y = it.multi_index
        rojo, _, azul = imagen_arreglo[x,y, :]
        
        # Calcula el cociente R/B (evita la división por cero).
        cociente = rojo / (azul + 1e-6)

        if cociente < umbral:
            color = (0, 0, 0)  # Negro "cielo"
        else:
            color = (255, 255, 255)  # Blanco "nube"

        imagen_BN.point((y, x), color)
        
        it.iternext()

    return imagen_BN