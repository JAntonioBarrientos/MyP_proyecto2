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
    print('Este es el CCI de tu imagen:',calcular_CCI(imagen))
    
    if bandera_s:
        nuevo_nombre = f"{nombre_imagen.split('.')[0]}-seg.png"
        imagen.save(nuevo_nombre)


if __name__ == "__main__":
    main()