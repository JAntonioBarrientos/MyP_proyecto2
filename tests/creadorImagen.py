from PIL import Image, ImageDraw

def crear_imagen_test(ancho, alto):
    imagen = Image.new("RGB", (ancho, alto), color="white")
    draw = ImageDraw.Draw(imagen)
    draw.text((10, 10), "Test Image", fill="black")
    imagen.save("test.jpg")

if __name__ == "__main__":
    crear_imagen_test(100, 100)