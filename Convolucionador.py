from PIL import Image, ImageDraw

def proceso_Convolucionador(imagen_path):
    """
    Aplica una convolución a una imagen utilizando una máscara circular y la operación de votación.

    :param imagen_path: Ruta de la imagen de entrada.
    :return: Ruta de la imagen resultante.
    """
    imagen_con_opacidad = aplicar_mascara_a_imagen(imagen_path)

    ancho, alto = imagen_con_opacidad.size
    draw = ImageDraw.Draw(imagen_con_opacidad)

    for y in range(alto):
        for x in range(ancho):
            pixel = imagen_con_opacidad.getpixel((x, y))
            if pixel[3] != 0:
                vecinos = []
                for j in range(y - 1, y + 2):
                    for i in range(x - 1, x + 2):
                        if 0 <= i < ancho and 0 <= j < alto:
                            vecinos.append(imagen_con_opacidad.getpixel((i, j)))

                for j in range(y - 2, y + 3):
                    for i in range(x - 2, x + 3):
                        if (i < x - 1 or i > x + 1 or j < y - 1 or j > y + 1) and 0 <= i < ancho and 0 <= j < alto:
                            vecinos.append(imagen_con_opacidad.getpixel((i, j)))

                resultado = proceso_Votacion(vecinos)

                if 0 <= resultado <= 7:
                    draw.point((x, y), fill=(0, 0, 0, 255))  # Negro
                elif 16 < resultado <= 25:
                    draw.point((x, y), fill=(255, 255, 255, 255))  # Blanco

    resultado_path = 'imagen_convolucionada.png'
    imagen_con_opacidad.save(resultado_path)
    return resultado_path

def proceso_Votacion(pixel_y_vecinos):
    """
    Realiza una operación de votación para contar píxeles blancos en la lista de vecinos.

    :param pixel_y_vecinos: Lista de píxeles y sus vecinos.
    :return: Conteo de píxeles blancos.
    """
    conteo_blancos = 0

    for pixel in pixel_y_vecinos:
        if pixel[:3] == (255, 255, 255):
            conteo_blancos += 1

    return conteo_blancos

def aplicar_mascara_a_imagen(imagen_path):
    """
    Abre una imagen PNG, crea una máscara circular y aplica la máscara como máscara de opacidad a la imagen original.

    :param imagen_path: Ruta de la imagen de entrada.
    :return: Imagen con la máscara de opacidad aplicada.
    """
    imagen = Image.open(imagen_path)
    ancho, alto = imagen.size
    mascara = Image.new('L', (ancho, alto), 0)
    dibujo = ImageDraw.Draw(mascara)
    radio = 1324
    centro = (ancho // 2, alto // 2)
    dibujo.ellipse((centro[0] - radio, centro[1] - radio, centro[0] + radio, centro[1] + radio), fill=255)
    imagen.putalpha(mascara)
    return imagen
