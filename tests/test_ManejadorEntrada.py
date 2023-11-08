import unittest
from unittest.mock import patch
from io import StringIO
from ManejadorEntrada import verificar_imagen, manejar_entrada, ErrorFormato, ErrorDimension

class TestVerificarImagen(unittest.TestCase):

    def test_verificar_imagen_correcta(self):
        self.assertTrue(verificar_imagen("test.jpg", 100, 100))

    def test_verificar_imagen_formato_incorrecto(self):
        with self.assertRaises(ErrorFormato):
            verificar_imagen("test.png", 100, 100)

    def test_verificar_imagen_dimensiones_incorrectas(self):
        with self.assertRaises(ErrorDimension):
            verificar_imagen("test.jpg", 200, 200)

class TestManejarEntrada(unittest.TestCase):

    @patch('sys.argv', ['script_name', 'test.jpg', '-s'])
    def test_manejar_entrada_con_bandera_s(self):
        nombre_imagen, bandera_s = manejar_entrada()
        self.assertEqual(nombre_imagen, 'test.jpg')
        self.assertTrue(bandera_s)

    @patch('sys.argv', ['script_name', 'test.jpg'])
    def test_manejar_entrada_sin_bandera_s(self):
        nombre_imagen, bandera_s = manejar_entrada()
        self.assertEqual(nombre_imagen, 'test.jpg')
        self.assertFalse(bandera_s)

    @patch('sys.argv', ['script_name'])
    def test_manejar_entrada_sin_argumentos(self):
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            nombre_imagen, bandera_s = manejar_entrada()
            self.assertIsNone(nombre_imagen)
            self.assertFalse(bandera_s)
            self.assertEqual(mock_stdout.getvalue().strip(), "Por favor, proporciona el nombre de una imagen.")

if __name__ == '__main__':
    unittest.main()