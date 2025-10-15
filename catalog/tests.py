from django.test import TestCase
from .models import Category, Product


class CatalogModelTests(TestCase):
    def test_category_creation(self):
        """Category modeli doğru oluşturulur"""
        category = Category.objects.create(
            name="TCG Kartları",
            slug="tcg-kartlari",
            description="Trading Card Game kartları"
        )
        self.assertEqual(str(category), "TCG Kartları")
        self.assertEqual(category.slug, "tcg-kartlari")

    def test_product_creation(self):
        """Product modeli doğru oluşturulur"""
        category = Category.objects.create(
            name="TCG Kartları",
            slug="tcg-kartlari"
        )
        product = Product.objects.create(
            name="Pokémon Base Set",
            slug="pokemon-base-set",
            category=category,
            brand="Pokémon"
        )
        self.assertEqual(str(product), "Pokémon Base Set (Pokémon)")
        self.assertEqual(product.category, category)