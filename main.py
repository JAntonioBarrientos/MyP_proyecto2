from Convolucionador import proceso_Convolucionador, aplicar_mascara_a_imagen
from PIL import Image, ImageDraw

def main():
    """
    Funcion principal del programa.

    Ejecuta mediante los demás funciones definidas en los demas archivos 
    el proceso para validar la entrada, recortar la imágen, aplicarle un filtro
    para discernir entre pixeles 'nube' o 'cielo', convolucionar la imágen, aplicarle una
    mascara, calcular el CCI y regresar dichos valores.
    """

    ancho_imagen = 4368
    largo_imagen = 2912
    centro_circulo = (2184,1456)
    radio_circulo = 1324

    imagen_path = 'imagenBN.png'  # Reemplaza con la ruta de tu imagen
    imagen = Image.open(imagen_path)
    imagen = aplicar_mascara_a_imagen(imagen, radio_circulo)
    imagen2 = proceso_Convolucionador(imagen)
    imagen2.save('imagen2.png')

    

if __name__ == "__main__":
    main()
