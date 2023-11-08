from PIL import Image, ImageDraw

def proceso_Convolucionador(imagen):
    """
    Aplica un proceso de convolución a una imagen.

    Args:
        imagen (PIL.Image.Image): La imagen a procesar.

    Returns:
        PIL.Image.Image: La imagen procesada.

    Realiza un proceso de convolución en la imagen, donde cada píxel se evalúa
    en función de los valores de sus vecinos y se aplica una regla de votación
    para determinar su nuevo valor.
    
    Se utiliza una matriz 5x5 para este proceso, se probo con una matriz 3x3 pero
    no daba los resultados deseados.
    """
    
    ancho, alto = imagen.size
    draw = ImageDraw.Draw(imagen)

    for y in range(alto):
        for x in range(ancho):
            pixel = imagen.getpixel((x, y))
            if pixel[3] != 0:
                vecinos = []
                for j in range(y - 1, y + 2):
                    for i in range(x - 1, x + 2):
                        if 0 <= i < ancho and 0 <= j < alto:
                            pixelVecino = imagen.getpixel((i, j))
                            if pixelVecino[3] != 0:
                                vecinos.append(pixelVecino)

                for j in range(y - 2, y + 3):
                    for i in range(x - 2, x + 3):
                        if (i < x - 1 or i > x + 1 or j < y - 1 or j > y + 1) and 0 <= i < ancho and 0 <= j < alto:
                            pixelVecino = imagen.getpixel((i, j))
                            if pixelVecino[3] != 0:
                                vecinos.append(pixelVecino)

                resultado = proceso_Votacion(vecinos)

                if 0 <= resultado <= 7:
                    draw.point((x, y), fill=(0, 0, 0, 255))  # Negro
                elif 16 < resultado <= 25:
                    draw.point((x, y), fill=(255, 255, 255, 255))  # Blanco

    return imagen

def proceso_Votacion(pixel_y_vecinos):
    """
    Realiza un proceso de votación en una lista de píxeles.

    Args:
        pixel_y_vecinos (list): Lista de píxeles y sus vecinos.

    Returns:
        int: El resultado del proceso de votación.

    El proceso de votación cuenta cuántos píxeles blancos hay en la lista de
    píxeles y devuelve el recuento.
    """
    
    conteo_blancos = 0

    for pixel in pixel_y_vecinos:
        if pixel[:3] == (255, 255, 255):
            conteo_blancos += 1

    return conteo_blancos

def aplicar_mascara_a_imagen(imagen, radio):
    """
    Aplica una máscara elíptica a una imagen.

    Args:
        imagen (PIL.Image.Image): La imagen a la que se aplicará la máscara.
        radio (int): El radio de la máscara elíptica.

    Returns:
        PIL.Image.Image: La imagen con la máscara aplicada.

    Crea una máscara elíptica y la aplica a la imagen, dejando solo visible la
    parte de la imagen que coincide con la máscara.
    """
    
    ancho, alto = imagen.size
    centro = (ancho // 2, alto // 2)
    mascara = Image.new('L', (ancho, alto), 0)
    dibujo = ImageDraw.Draw(mascara)
    dibujo.ellipse((centro[0] - radio, centro[1] - radio, centro[0] + radio, centro[1] + radio), fill=255)
    imagen.putalpha(mascara)
    return imagen
