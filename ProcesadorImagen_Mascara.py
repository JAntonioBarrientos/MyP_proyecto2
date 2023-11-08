from PIL import Image, ImageDraw

def imagen_mascara(nombre_imagen):
    """
    Crea una imagen con una máscara elíptica y recorta la imagen de entrada con esa máscara.

    :param archivo: Imagen de entrada.
    :type archivo: str
    :return: Imagen recortada con la máscara elíptica.
    :rtype: PIL.Image.Image
    """

    imagen = Image.open(nombre_imagen)
    ancho, alto = imagen.size

    centro_x = ancho // 2
    centro_y = alto // 2
    radio = 1324

    mascara = Image.new('L', (ancho, alto), 0)
    draw = ImageDraw.Draw(mascara)
    draw.ellipse((centro_x - radio, centro_y - radio, centro_x + radio, centro_y + radio), fill=255)
    imagen_recortada = Image.new('RGB', (ancho, alto))
    imagen_recortada.paste(imagen, mask=mascara)
    
    return imagen_recortada