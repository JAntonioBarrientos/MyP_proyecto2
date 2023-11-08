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
            verificar_imagen("tests/test.png", 100, 100)


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
