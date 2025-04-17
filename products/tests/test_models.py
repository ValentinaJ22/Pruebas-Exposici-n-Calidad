from django.test import TestCase
from products.models import Product
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils.text import slugify
from django.core.exceptions import ValidationError
import uuid

class ProductStatementCoverageTests(TestCase):

    def get_test_image(self):
        return SimpleUploadedFile(name='test.jpg', content=b'image data', content_type='image/jpeg')

    def test_slug_set_if_not_provided(self):
        """🧪 Cubre las sentencias dentro del if"""
        product = Product.objects.create(
            title="Producto único",
            description="desc",
            image=self.get_test_image()
        )
        expected_slug = slugify("Producto único")
        self.assertEqual(product.slug, expected_slug)

    def test_slug_not_changed_if_already_set(self):
        """🧪 Cubre else implícito (no entra al if)"""
        product = Product.objects.create(
            title="Título",
            description="desc",
            price=12.5,
            slug="ya-existe",  # Asegúrate de probar un slug explícito aquí
            image=self.get_test_image()
        )
        self.assertEqual(product.slug, "ya-existe")

    def test_slug_while_loop_runs_when_conflict(self):
        """🧪 Cubre el while y re-generación del slug"""
        title = "Producto repetido"

        product1 = Product.objects.create(
            title=title,
            description="desc",
            image=self.get_test_image()
        )

        product2 = Product.objects.create(
            title=title,
            description="desc",
            image=self.get_test_image()
        )

        # Verifica que los slugs comienzan con el título y no son iguales
        self.assertTrue(product2.slug.startswith(slugify(title)))
        self.assertNotEqual(product1.slug, product2.slug)  # Verifica que sean diferentes

    def test_all_fields_saved_correctly(self):
        """🧪 Cubre todas las sentencias de campos"""
        product = Product.objects.create(
            title="Título",
            description="Una descripción larga",
            price=123.45,
            image=self.get_test_image()
        )
        self.assertEqual(product.title, "Título")
        self.assertEqual(product.description, "Una descripción larga")
        self.assertEqual(float(product.price), 123.45)
        self.assertIsNotNone(product.created_at)
        self.assertTrue(product.image)

    def test_title_too_long_raises_error(self):
        """🧪 Cubre validación de longitud máxima"""
        product = Product(
            title="x" * 51,
            description="desc",
            image=self.get_test_image()
        )
        with self.assertRaises(ValidationError):
            product.full_clean()

    def test_missing_required_image(self):
   
     product = Product(
          title="Sin imagen",
          description="desc"
     )
     try:
        product.save()
        saved_product = Product.objects.get(title="Sin imagen")
        self.assertTrue(saved_product)  # Verifica que el producto fue guardado
     except Exception as e:
        # Si el modelo lanza algún tipo de excepción diferente, se maneja aquí
        print(f"Excepción durante la prueba: {e}")
        self.fail(f"Expected a ValueError, but got {type(e).__name__}")

