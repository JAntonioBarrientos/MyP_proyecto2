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
    # EN PROCESO 
    cci = pixeles_nube / total_pixeles
    return cci