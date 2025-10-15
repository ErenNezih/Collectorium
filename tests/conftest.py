"""
Pytest configuration and fixtures for Collectorium tests.

This file contains shared fixtures and configurations used across all tests.
"""

import pytest
from django.contrib.auth import get_user_model
from stores.models import Store
from catalog.models import Category, Product
from listings.models import Listing, ListingImage
from cart.cart import Cart
from decimal import Decimal

User = get_user_model()


@pytest.fixture
def buyer_user(db):
    """Create a buyer user for testing."""
    return User.objects.create_user(
        username='buyer_test',
        email='buyer@test.com',
        password='testpass123',
        role='buyer'
    )


@pytest.fixture
def seller_user(db):
    """Create a seller user for testing."""
    return User.objects.create_user(
        username='seller_test',
        email='seller@test.com',
        password='testpass123',
        role='seller'
    )


@pytest.fixture
def store(db, seller_user):
    """Create a store for testing."""
    return Store.objects.create(
        owner=seller_user,
        name="Test Store",
        slug="test-store",
        bio="This is a test store",
        is_verified=True
    )


@pytest.fixture
def category(db):
    """Create a category for testing."""
    return Category.objects.create(
        name="Trading Cards",
        slug="trading-cards",
        description="TCG and collectible cards"
    )


@pytest.fixture
def product(db, category):
    """Create a product for testing."""
    return Product.objects.create(
        name="Blue-Eyes White Dragon",
        slug="blue-eyes-white-dragon",
        category=category,
        brand="Konami",
        description="Legendary dragon card"
    )


@pytest.fixture
def listing(db, store, product):
    """Create a listing for testing."""
    return Listing.objects.create(
        store=store,
        product=product,
        title="Blue-Eyes White Dragon - Mint Condition",
        description="Perfect condition, first edition",
        price=Decimal('150.00'),
        currency='TRY',
        condition='new',
        stock=1,
        is_active=True
    )


@pytest.fixture
def cart_session(client):
    """Create a cart session for testing."""
    return Cart(client)


@pytest.fixture
def authenticated_buyer_client(client, buyer_user):
    """Client authenticated as buyer."""
    client.force_login(buyer_user)
    return client


@pytest.fixture
def authenticated_seller_client(client, seller_user):
    """Client authenticated as seller."""
    client.force_login(seller_user)
    return client

