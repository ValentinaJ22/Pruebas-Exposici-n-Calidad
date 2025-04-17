from django.test import TestCase
from products.models import Product
from users.models import User
from carts.models import Cart, CartProducts
from decimal import Decimal

class CartTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser', email='test@example.com')
        self.product1 = Product.objects.create(title="Test Product 1", price=Decimal(10.00))
        self.product2 = Product.objects.create(title="Test Product 2", price=Decimal(15.00))
        self.cart = Cart.objects.create(user=self.user)

    def test_update_subtotal_correct(self):
        # 2*10 + 3*15 = 65
        CartProducts.objects.create(cart=self.cart, product=self.product1, quantity=2)
        CartProducts.objects.create(cart=self.cart, product=self.product2, quantity=3)

        self.cart.update_subtotal()
        self.cart.refresh_from_db()

        expected_subtotal = Decimal(65.00)
        self.assertEqual(self.cart.subtotal, expected_subtotal)

    def test_update_subtotal_incorrect(self):
        # 2*10 + 3*15 = 65, pero lo comparamos contra 50
        CartProducts.objects.create(cart=self.cart, product=self.product1, quantity=2)
        CartProducts.objects.create(cart=self.cart, product=self.product2, quantity=3)

        self.cart.update_subtotal()
        self.cart.refresh_from_db()

        wrong_subtotal = Decimal(50.00)
        self.assertNotEqual(self.cart.subtotal, wrong_subtotal)

    def test_update_total_correct(self):
        # Establecer un subtotal manualmente
        self.cart.subtotal = Decimal('100.00')  # subtotal manual
        self.cart.update_total()  # Llamar a la función que calcula el total

        # Calcular el total esperado, que es el subtotal más el 5% de comisión
        expected_total = Decimal('105.00')  # 100 * 1.05 = 105

        # Actualizar el objeto del carrito desde la base de datos para obtener los datos más recientes
        self.cart.refresh_from_db()

        # Verificar que el total calculado coincida con el valor esperado
        self.assertEqual(self.cart.total, expected_total)

    def test_update_total_incorrect(self):
        # Establecer un subtotal manualmente
        self.cart.subtotal = Decimal('100.00')  # subtotal manual
        self.cart.update_total()  # Llamar a la función que calcula el total

        # Calcular el total esperado, que es el subtotal más el 5% de comisión
        expected_total = Decimal('100.00')  # 100 * 1.05 = 105

        # Actualizar el objeto del carrito desde la base de datos para obtener los datos más recientes
        self.cart.refresh_from_db()

        # Verificar que el total calculado no coincida con el valor esperado
        self.assertNotEqual(self.cart.total, expected_total)

    def test_update_quantity(self):
         # Crear un objeto CartProducts en el carrito con una cantidad inicial
        self.cart_product = CartProducts.objects.create(cart=self.cart, product=self.product1, quantity=1)
        # Verifica que la cantidad inicial de cart_product sea 1
        self.assertEqual(self.cart_product.quantity, 1)

        # Actualiza la cantidad usando el método
        self.cart_product.update_quantity(5)

        # Verifica que la cantidad se actualiza correctamente a 5
        self.cart_product.refresh_from_db()  # Recarga el objeto desde la base de datos
        self.assertEqual(self.cart_product.quantity, 5)

     
