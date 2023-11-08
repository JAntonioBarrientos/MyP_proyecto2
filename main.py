import sys

from ManejadorEntrada import verificar_imagen, ErrorFormato, ErrorDimension, manejar_entrada

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

if __name__ == "__main__":
    main()