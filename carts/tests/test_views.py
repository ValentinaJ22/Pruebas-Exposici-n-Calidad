from django.urls import reverse
from django.test import TestCase
from carts.models import Cart
from products.models import Product
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from decimal import Decimal

User = get_user_model()

class CartRemoveTestCase(TestCase):
    def setUp(self):
        
        self.client = self.client_class()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')

        # Crear imagen simulada
        image = SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg')

        # Crear producto
        self.product = Product.objects.create(title="Mesa", description="Mesa de madera", price=Decimal(15.00), image=image)

        # Accedemos a la vista del carrito para que se cree el carrito correctamente
        self.client.get(reverse('carts:cart'))

        # Ahora obtenemos el carrito como lo haría la vista
        self.cart = Cart.objects.get(user=self.user)
        self.cart.products.add(self.product)

    #  Prueba que verifica que un producto puede ser eliminado del carrito correctamente.
    def test_remove_product_from_cart(self):

         # Verificar que el producto está inicialmente en el carrito
        self.assertIn(self.product, self.cart.products.all())

        # Enviar solicitud POST para eliminar el producto
        response = self.client.post(reverse('carts:remove'), {'product_id': self.product.id})

        # Confirmar redirección
        self.assertEqual(response.status_code, 302)

        # Actualizar carrito
        self.cart.refresh_from_db()

        # Verificar que ya no esté
        self.assertNotIn(self.product, self.cart.products.all())

    # Intentar eliminar un producto con ID inválido debería devolver 404.
    def test_remove_invalid_product(self):
        
        invalid_id = 99999  # supondremos que este ID no existe
        response = self.client.post(reverse('carts:remove'), {'product_id': invalid_id})
        self.assertEqual(response.status_code, 404)

   



    # # Prueba con product_id vacío
    # def test_remove_product_with_empty_id(self):
    #     response = self.client.post(reverse('carts:remove'), {'product_id': ''})
    #     self.assertEqual(response.status_code, 400)
    #     self.assertContains(response, 'ID de producto inválido')

    # # Prueba con un product_id no numérico
    # def test_remove_product_with_invalid_id(self):
    #     response = self.client.post(reverse('carts:remove'), {'product_id': 'abc'})
    #     self.assertEqual(response.status_code, 400)
    #     self.assertContains(response, 'ID de producto inválido')

    # # Prueba con product_id None
    # def test_remove_product_with_none_id(self):
    #     response = self.client.post(reverse('carts:remove'), {'product_id': None})
    #     self.assertEqual(response.status_code, 400)
    #     self.assertContains(response, 'ID de producto inválido')

    
    


