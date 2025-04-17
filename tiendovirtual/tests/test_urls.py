from django.urls import reverse, resolve
from django.test import TestCase

class TestUrls(TestCase):  # Hereda de TestCase

    # Test para la url de la página de inicio (index)
    def test_index_url(self):
        path = reverse('index')
        resolver = resolve(path)
        self.assertEqual(resolver.url_name, 'index')  # Usa assertEqual para pruebas

    # Test para la url de login
    def test_login_url(self):
        path = reverse('login')
        resolver = resolve(path)
        self.assertEqual(resolver.url_name, 'login')

    # Test para la url de logout
    def test_logout_url(self):
        path = reverse('logout')
        resolver = resolve(path)
        self.assertEqual(resolver.url_name, 'logout')

    # Test para la url de registro
    def test_register_url(self):
        path = reverse('register')
        resolver = resolve(path)
        self.assertEqual(resolver.url_name, 'register')

    def test_product_search_url(self):
          path = reverse('products:search')  # Usamos el nombre 'search' dentro de la app 'products'
          resolver = resolve(path)
          self.assertEqual(resolver.url_name, 'search')

    def test_product_detail_url(self):
          path = reverse('products:product', kwargs={'slug': 'example-product'})  # Usamos el nombre 'product' y pasamos un slug
          resolver = resolve(path)
          self.assertEqual(resolver.url_name, 'product')

 
    def test_cart_url(self):
          path = reverse('carts:cart')  # Usamos el nombre de la URL definida con el namespace 'carts'
          resolver = resolve(path)
          self.assertEqual(resolver.url_name, 'cart')

    # Test para la url de orden
    def test_order_url(self):
        path = reverse('orders:order')  # Usamos el nombre de la URL definida
        resolver = resolve(path)
        self.assertEqual(resolver.url_name, 'order')
