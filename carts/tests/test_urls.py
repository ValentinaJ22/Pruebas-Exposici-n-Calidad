from django.urls import reverse, resolve
from django.test import TestCase

class TestUrls(TestCase):

    # Prueba para la URL de carrito
    def test_cart_url(self):
        path = reverse('carts:cart')  # OK: reverse sí usa 'carts:cart'
        resolver = resolve(path)
        self.assertEqual(resolver.url_name, 'cart')  # SIN prefijo

    # Prueba para la URL de agregar
    def test_add_url(self):
        path = reverse('carts:add')
        resolver = resolve(path)
        self.assertEqual(resolver.url_name, 'add')  # SIN prefijo

    # Prueba para la URL de eliminar
    def test_remove_url(self):
        path = reverse('carts:remove')
        resolver = resolve(path)
        self.assertEqual(resolver.url_name, 'remove')  # SIN prefijo




