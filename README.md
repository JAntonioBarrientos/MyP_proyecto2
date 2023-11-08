# MyP_proyecto2 Cobertura Nubosa

## Integrantes del Equipo
* Barrientos Sánchez José Antonio 423019269
* Morales Chaparro Gael Antonio - 320076972
* Sosa Romo Juan Mario - 320051926
* Pastor De La Cruz Miguel - 320125537

## Descripción
Este proyecto tiene como objetivo calcular el Índice de Cobertura Nubosa (CCI) en imágenes del cielo capturadas mediante una camara. Además, opcionalmente, permite generar una imagen en blanco y negro que destaque las áreas de nubes y cielo en la fotografía.

## Requisitos

- Python 3
- Tener las bibliotecas necesarias. Esto se puede ejecutar mediante:
```bash
    pip install -r requirements.txt
```

## Uso


Ejecute el programa principal main.py proporcionando el nombre del archivo de imagen de entrada la cual debe estar en la raiz del repositorio, en formato JPEG. Puedes incluir la bandera opcional "S", "s", "-s" o "-S"  al final para generar la imagen en blanco y negro.


Ejemplo:

```bash
python3 main.py IMAGEN.jpg S
python3 main.py IMAGEN.jpg s
python3 main.py IMAGEN.jpg

```

## Pruebas unitarias
Para correr las pruebas unitarias ejecute el comando:

```bash
python3 -m unittest tests.test_ManejadorEntrada
```


## Estructura del proyecto

1.  `main.py:` Programa principal para ejecutar el proyecto.
2.  `CalculadorCCI.py`: Calcula el Índice de Cobertura Nubosa (CCI) a partir de la imagen procesada.
3.  `Convolucionador.py`: Aplica una matriz de convolución a la imagen binaria.
4.  `FiltroRB_ClasificadorPixeles.py`: Clasifica los píxeles de la imagen como nubes o cielo.
5.  `ManejadorEntrada.py`: Gestiona la validación de la entrada, la comprobación de la bandera y las dimensiones de la imagen.
6.  `ProcesadorImagen_Macara.py`: Aplica una máscara a la imagen para cubrir solo la parte útil.

## Bibliotecas:

- PILLOW: https://pillow.readthedocs.io/en/stable/
- NumPy: https://numpy.org/doc/stable/






