"""
Tests for Order functionality.
"""

import pytest
from orders.models import Order, OrderItem
from decimal import Decimal


@pytest.mark.django_db
class TestOrderModel:
    """Test Order model functionality."""
    
    def test_create_order(self, buyer_user):
        """Test creating an order."""
        order = Order.objects.create(
            buyer=buyer_user,
            total=Decimal('150.00'),
            currency='TRY',
            status='pending',
            shipping_address="Test Address, Istanbul"
        )
        assert order.buyer == buyer_user
        assert order.total == Decimal('150.00')
        assert order.status == 'pending'
    
    def test_order_with_items(self, buyer_user, listing):
        """Test creating an order with items."""
        order = Order.objects.create(
            buyer=buyer_user,
            total=listing.price,
            shipping_address="Test Address"
        )
        
        order_item = OrderItem.objects.create(
            order=order,
            listing=listing,
            quantity=1,
            price_snapshot=listing.price
        )
        
        assert order.items.count() == 1
        assert order_item.price_snapshot == listing.price


@pytest.mark.django_db
class TestCheckoutFlow:
    """Test end-to-end checkout flow."""
    
    def test_checkout_requires_login(self, client):
        """Test that checkout requires authentication."""
        response = client.get('/orders/checkout/')
        assert response.status_code == 302  # Redirect to login
    
    def test_checkout_with_cart(self, authenticated_buyer_client, listing):
        """Test checkout process with items in cart."""
        # Add to cart
        authenticated_buyer_client.post(
            f'/cart/add/{listing.id}/',
            {'quantity': 1, 'override': False}
        )
        
        # Access checkout
        response = authenticated_buyer_client.get('/orders/checkout/')
        assert response.status_code == 200

