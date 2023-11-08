def calcular_CCI(imagen_convolucion):
    """
    Calcula el Índice de Cobertura de Nubes (CCI) en una imagen de convolución.

    El CCI se calcula dividiendo el número de píxeles que representan nubes en la imagen
    entre el total de píxeles en la imagen.

    :param imagen_convolucion: Imagen de convolución que representa la cobertura de nubes.
    :type imagen_convolucion: PIL.Image.Image
    :return: Índice de Cobertura de Nubes (CCI) de la imagen.
    :rtype: float
    """
    ancho, alto = imagen_convolucion.size
    total_pixeles = 0
    pixeles_blancos = 0

    for y in range(alto):
        for x in range(ancho):
            pixel = imagen_convolucion.getpixel((x, y))
            if pixel[3] != 0:
                total_pixeles += 1
                if pixel == (255, 255, 255, 255):  # Suponiendo que 255 representa blanco en tu imagen en blanco y negro
                    pixeles_blancos += 1

    if total_pixeles == 0:
        return 0.0
    else:
        cci = pixeles_blancos / total_pixeles
        return cci