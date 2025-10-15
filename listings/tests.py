from django.test import TestCase
from django.contrib.auth import get_user_model
from stores.models import Store
from catalog.models import Category, Product
from .models import Listing

User = get_user_model()


class ListingModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.store = Store.objects.create(
            owner=self.user,
            name="Test Mağaza",
            slug="test-magaza"
        )
        self.category = Category.objects.create(
            name="TCG Kartları",
            slug="tcg-kartlari"
        )
        self.product = Product.objects.create(
            name="Pokémon Base Set",
            slug="pokemon-base-set",
            category=self.category,
            brand="Pokémon"
        )

    def test_listing_creation(self):
        """Listing modeli doğru oluşturulur"""
        listing = Listing.objects.create(
            store=self.store,
            product=self.product,
            title="Pokémon Charizard",
            description="Nadir Charizard kartı",
            price=500.00,
            condition="good",
            stock=1
        )
        self.assertEqual(str(listing), "Pokémon Charizard")
        self.assertEqual(listing.store, self.store)
        self.assertEqual(listing.product, self.product)
        self.assertTrue(listing.is_active)