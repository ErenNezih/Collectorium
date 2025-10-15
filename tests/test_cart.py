"""
Tests for Cart functionality.
"""

import pytest
from cart.cart import Cart
from decimal import Decimal


@pytest.mark.django_db
class TestCart:
    """Test Cart session-based functionality."""
    
    def test_add_to_cart(self, client, listing):
        """Test adding a listing to cart."""
        cart = Cart(client)
        cart.add(listing, quantity=1)
        
        assert len(cart) == 1
        assert cart.get_total_price() == listing.price
    
    def test_add_multiple_items(self, client, listing):
        """Test adding multiple quantities."""
        cart = Cart(client)
        cart.add(listing, quantity=2)
        
        assert len(cart) == 2
        assert cart.get_total_price() == listing.price * 2
    
    def test_remove_from_cart(self, client, listing):
        """Test removing from cart."""
        cart = Cart(client)
        cart.add(listing, quantity=1)
        cart.remove(listing)
        
        assert len(cart) == 0
    
    def test_clear_cart(self, client, listing):
        """Test clearing entire cart."""
        cart = Cart(client)
        cart.add(listing, quantity=2)
        cart.clear()
        
        assert len(cart) == 0


@pytest.mark.django_db
class TestCartViews:
    """Test cart views."""
    
    def test_cart_detail_view(self, client):
        """Test cart detail page."""
        response = client.get('/cart/')
        assert response.status_code == 200
    
    def test_add_to_cart_view(self, client, listing):
        """Test adding to cart via POST."""
        response = client.post(
            f'/cart/add/{listing.id}/',
            {'quantity': 1, 'override': False}
        )
        assert response.status_code == 302  # Redirect after add

