from PIL import Image, ImageDraw

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