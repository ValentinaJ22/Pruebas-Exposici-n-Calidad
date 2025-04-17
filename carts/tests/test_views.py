from django.test import TestCase
from django.urls import reverse
from products.models import Product
from carts.models import Cart, CartProducts
from django.contrib.auth.models import User

class TestCartViews(TestCase):

    def setUp(self):
        # Crear un producto de prueba con el modelo correcto
        self.product = Product.objects.create(
            title="Test Product",
            description="This is a test product.",
            price=10.0,
            slug="test-product",
            image="path/to/image.jpg"
        )

        # Crear un carrito de prueba (sin usuario para simplicidad)
        self.cart = Cart.objects.create(user=None)  

    def test_cart_view(self):
        # Probar la vista de ver el carrito
        response = self.client.get(reverse('carts:cart'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Product")  # Asegurarse de que el producto esté en el carrito
        self.assertContains(response, "10.00")  # Asegurarse de que el precio del producto esté visible

    def test_add_view(self):
        # Probar agregar un producto al carrito
        response = self.client.post(reverse('carts:add'), {
            'product_id': self.product.id,
            'quantity': 2
        })
        self.assertEqual(response.status_code, 200)  # Verificar que la respuesta sea correcta
        # Verificar si el producto se ha agregado correctamente
        cart_product = CartProducts.objects.get(cart=self.cart, product=self.product)
        self.assertEqual(cart_product.quantity, 2)

    def test_remove_view(self):
        # Primero, agregar el producto al carrito
        self.client.post(reverse('carts:add'), {
            'product_id': self.product.id,
            'quantity': 1
        })

        # Verificar que el producto se haya agregado
        cart_product = CartProducts.objects.get(cart=self.cart, product=self.product)
        self.assertEqual(cart_product.quantity, 1)

        # Ahora eliminar el producto del carrito
        response = self.client.post(reverse('carts:remove'), {
            'product_id': self.product.id
        })
        self.assertEqual(response.status_code, 302)  # Verificar que se redirige después de eliminar
        # Verificar que el producto haya sido eliminado
        with self.assertRaises(CartProducts.DoesNotExist):
            CartProducts.objects.get(cart=self.cart, product=self.product)
