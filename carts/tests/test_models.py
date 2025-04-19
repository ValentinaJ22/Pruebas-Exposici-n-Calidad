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
        self.product_free = Product.objects.create(title="Free Product", price=Decimal('0.00'))
        self.cart = Cart.objects.create(user=self.user)

    # Prueba del calculo del subtotal cuando mas de 1 producto en el carrito   
    def test_update_subtotal(self):
    
        CartProducts.objects.create(cart=self.cart, product=self.product1, quantity=2)
        CartProducts.objects.create(cart=self.cart, product=self.product2, quantity=3)

        self.cart.update_subtotal()
        self.cart.refresh_from_db()
        # 2*10 + 3*15 = 65

        expected_subtotal = Decimal(65.00)
        self.assertEqual(self.cart.subtotal, expected_subtotal)

    #Prueba cuando el carrito esta vacio
    def test_empty_cart_subtotal(self):
       
        self.cart.update_subtotal()
        self.cart.refresh_from_db()
        self.assertEquals(self.cart.subtotal, 0)


    # #Prueba cuando hay un solo producto
    # def test_single_product_subtotal(self):

    #     CartProducts.objects.create(cart=self.cart, product=self.product1, quantity=2)
    #     self.cart.update_subtotal()
    #     self.cart.refresh_from_db()
    #     expected_subtotal = Decimal(20.00)
    #     self.assertEqual(self.cart.subtotal, expected_subtotal)

    # #Prueba cuando un producto tiene cantidad 0
    # def test_zero_quantity_subtotal(self):
       
    #     CartProducts.objects.create(cart=self.cart, product=self.product1, quantity=0)
    #     self.cart.update_subtotal()
    #     self.cart.refresh_from_db()
    #     self.assertEqual(self.cart.subtotal, 0)

    # #Prueba cuando un producto tiene precio 0
    # def test_free_product_subtotal(self):
        
    #     CartProducts.objects.create(cart=self.cart, product=self.product_free, quantity=5)
    #     self.cart.update_subtotal()
    #     self.cart.refresh_from_db()
    #     self.assertEqual(self.cart.subtotal, Decimal('0.00'))



    