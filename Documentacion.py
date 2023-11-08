from Convolucionador import proceso_Convolucionador
from ProcesadorImagen_Mascara import aplicar_mascara_a_imagen
from FiltroRB_ClasificadorPixeles import procesa_imagen_a_blanco_y_negro
from RecortadorImagen import recortar
from CalculadorCCI import  calcular_CCI
from PIL import Image
from ManejadorEntrada import verificar_imagen, ErrorFormato, ErrorDimension, manejar_entrada

def main():
    """
    Función principal del programa.

    Ejecuta el proceso completo para validar la entrada de la imagen, recortarla,
    aplicar un filtro para discernir entre pixeles 'nube' o 'cielo', convolucionar la imagen,
    aplicarle una máscara, calcular el CCI y guardar la imagen resultante.

    Args:
        None

    Returns:
        None

    Raises:
        None
    """

    ancho_imagen = 4368
    largo_imagen = 2912
    centro_circulo = (2184,1456)
    radio_circulo = 1324
    nombre_imagen, bandera_s = manejar_entrada()
    if nombre_imagen is None:
        return
    try:
        verificar_imagen(nombre_imagen, ancho_imagen, largo_imagen)
    except ErrorFormato as e:
        print(str(e))
        return
    except ErrorDimension as e:
        print(str(e))
        return
       
    imagen = Image.open(nombre_imagen)
    imagen = recortar(imagen, centro_circulo, radio_circulo)
    imagen = procesa_imagen_a_blanco_y_negro(imagen)
    imagen = aplicar_mascara_a_imagen(imagen, radio_circulo)
    imagen = imagen.convert('RGBA') 
    imagen = proceso_Convolucionador(imagen)
    print('Este es el CCI de tu imagen chiquibabi:',calcular_CCI(imagen))
    imagen.save('imagenFinal.png')

if __name__ == "__main__":
    main()

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

    return imagen

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

import unittest
from unittest.mock import patch
from io import StringIO
from ManejadorEntrada import verificar_imagen, manejar_entrada, ErrorFormato, ErrorDimension

class TestVerificarImagen(unittest.TestCase):

    def test_verificar_imagen_formato_incorrecto(self):
        """
        Prueba que la función verificar_imagen levanta un ErrorFormato para un formato incorrecto.
        """
        with self.assertRaises(ErrorFormato):
            verificar_imagen("test/test.png", 100, 100)

    def test_verificar_imagen_dimensiones_incorrectas(self):
        """
        Prueba que la función verificar_imagen levanta un ErrorDimension para dimensiones incorrectas.
        """
        with self.assertRaises(ErrorDimension):
            verificar_imagen("tests/test.jpg", 200, 200)

class TestManejarEntrada(unittest.TestCase):

    @patch('sys.argv', ['script_name', 'test.jpg', 's'])
    def test_manejar_entrada_con_bandera_s_minuscula(self):
        """
        Prueba que la función manejar_entrada devuelve los valores correctos con la bandera '-s' en minúscula.
        """
        nombre_imagen, bandera_s = manejar_entrada()
        self.assertEqual(nombre_imagen, 'test.jpg')
        self.assertTrue(bandera_s)

    @patch('sys.argv', ['script_name', 'test.jpg', 'S'])
    def test_manejar_entrada_con_bandera_s_mayuscula(self):
        """
        Prueba que la función manejar_entrada devuelve los valores correctos con la bandera '-S' en mayúscula.
        """
        nombre_imagen, bandera_s = manejar_entrada()
        self.assertEqual(nombre_imagen, 'test.jpg')
        self.assertTrue(bandera_s)

    @patch('sys.argv', ['script_name', 'test.jpg'])
    def test_manejar_entrada_sin_bandera_s(self):
        """
        Prueba que la función manejar_entrada devuelve los valores correctos sin la bandera '-s'.
        """
        nombre_imagen, bandera_s = manejar_entrada()
        self.assertEqual(nombre_imagen, 'test.jpg')
        self.assertFalse(bandera_s)

    @patch('sys.argv', ['script_name'])
    def test_manejar_entrada_sin_argumentos(self):
        """
        Prueba que la función manejar_entrada imprime un mensaje adecuado sin argumentos.
        """
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            nombre_imagen, bandera_s = manejar_entrada()
            self.assertIsNone(nombre_imagen)
            self.assertFalse(bandera_s)
            self.assertEqual(mock_stdout.getvalue().strip(), "Por favor, proporciona el nombre de una imagen.")

if __name__== '__main__':
    unittest.main()


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


from PIL import Image, ImageDraw

def crear_imagen_test(ancho, alto):
    imagen = Image.new("RGB", (ancho, alto), color="white")
    draw = ImageDraw.Draw(imagen)
    draw.text((10, 10), "Test Image", fill="black")
    imagen.save("test.jpg")

if __name__ == "__main__":
    crear_imagen_test(100, 100)