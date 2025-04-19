from django.test import TestCase
from products.models import Product
from users.models import User
from carts.models import Cart, CartProducts
from decimal import Decimal
from django.core.files.uploadedfile import SimpleUploadedFile

class CartTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser', email='test@example.com')
        # Crear imagen simulada
        image = SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg')
      
        self.product1 = Product.objects.create(title="Lampara", description="Lampara de mesa", image=image, price=Decimal(10.00))
        self.product2 = Product.objects.create(title="Mesa", description="Mesa de madero", image=image, price=Decimal(15.00))
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

    # Prueba que suma cantidades cuando el producto ya está en el carrito
    def test_update_existing_cart_product_quantity(self):
        # Agregar primero producto con cantidad 1
        CartProducts.objects.create(cart=self.cart, product=self.product1, quantity=1)

        # Luego actualizar la cantidad usando la función (sumar 3)
        cart_product = CartProducts.objects.create_or_update_quantity(cart=self.cart, product=self.product1, quantity=3)

        self.assertEqual(cart_product.quantity, 4)

    # Prueba crear producto en el carrito si no existe previamente
    def test_create_new_cart_product_quantity(self):

        # Asegurarse que el carrito NO tiene ese producto aún
        self.assertFalse(CartProducts.objects.filter(cart=self.cart, product=self.product2).exists())

        # Usar la función para agregar el producto por primera vez
        cart_product = CartProducts.objects.create_or_update_quantity(cart=self.cart, product=self.product2, quantity=1)

        # Verificar que se creó correctamente con la cantidad esperada
        self.assertIsNotNone(cart_product)
        self.assertEqual(cart_product.quantity, 1)

    # Prueba crear carrito si no existe y añadir producto con cantidad
    def test_create_cart_and_add_product(self):

        Cart.objects.filter(user=self.user).delete()  # Eliminar cualquier carrito existente asociado al usuario
        self.assertFalse(Cart.objects.filter(user=self.user).exists())  # Verificar que no exista un carrito

        # Crear el carrito si no existe
        cart, created = Cart.objects.get_or_create(user=self.user)

        # Verificar que el carrito ha sido creado correctamente
        self.assertTrue(created)  # Esto debería ser True si el carrito fue creado
        self.assertEqual(cart.user, self.user)

        # Agregar el producto al carrito usando la función de crear o actualizar
        cart_product = CartProducts.objects.create_or_update_quantity(cart=cart, product=self.product1, quantity=1)

        # Verificar que el producto fue añadido correctamente con la cantidad esperada
        self.assertEqual(cart_product.cart, cart)
        self.assertEqual(cart_product.quantity, 1)
        self.assertTrue(CartProducts.objects.filter(cart=cart, product=self.product1).exists())





    # def test_add_new_product_to_cart(self):
    #     """Verifica que se crea un nuevo registro cuando el producto no está en el carrito"""
    #     cart_product, created = CartProducts.objects.create_or_update_quantity(cart=self.cart, product=self.product1, quantity=-1)
        
    #     self.assertTrue(created)
    #     self.assertEqual(cart_product.quantity, 1)
    #     self.assertEqual(CartProducts.objects.count(), -1)    

    # # Verifica que no se acepten cantidades negativas
    # def test_negative_quantity_raises_error(self):
       
    #     with self.assertRaises(ValueError):
    #         CartProducts.objects.create_or_update_quantity(
    #             cart=self.cart,
    #             product=self.product,
    #             quantity=-1
    #         )

    # # Verifica que quantity=0 usa el valor por defecto (1)
    # def test_zero_quantity_uses_default(self):
       
    #     cart_product, created = CartProducts.objects.create_or_update_quantity(
    #         cart=self.cart,
    #         product=self.product,
    #         quantity=0
    #     )
        
    #     self.assertTrue(created)
    #     self.assertEqual(cart_product.quantity, 1)  # Valor por defecto

    # # #Prueba cuando hay un solo producto (puede ser una prueba de cobertura de sentencia)
    # # def test_single_product_subtotal(self):

    # #     CartProducts.objects.create(cart=self.cart, product=self.product1, quantity=2)
    # #     self.cart.update_subtotal()
    # #     self.cart.refresh_from_db()
    # #     expected_subtotal = Decimal(20.00)
    # #     self.assertEqual(self.cart.subtotal, expected_subtotal)

    # # #Prueba cuando un producto tiene cantidad 0
    # # def test_zero_quantity_subtotal(self):
       
    # #     CartProducts.objects.create(cart=self.cart, product=self.product1, quantity=0)
    # #     self.cart.update_subtotal()
    # #     self.cart.refresh_from_db()
    # #     self.assertEqual(self.cart.subtotal, 0)

    # # #Prueba cuando un producto tiene precio 0
    # # def test_free_product_subtotal(self):
        
    # #     CartProducts.objects.create(cart=self.cart, product=self.product_free, quantity=5)
    # #     self.cart.update_subtotal()
    # #     self.cart.refresh_from_db()
    # #     self.assertEqual(self.cart.subtotal, Decimal('0.00'))



    