"""
Tests for Listing model and views.
"""

import pytest
from listings.models import Listing
from decimal import Decimal


@pytest.mark.django_db
class TestListingModel:
    """Test Listing model functionality."""
    
    def test_create_listing(self, store, product):
        """Test creating a listing."""
        listing = Listing.objects.create(
            store=store,
            product=product,
            title="Test Listing",
            description="Test description",
            price=Decimal('99.99'),
            currency='TRY',
            condition='new',
            stock=5
        )
        assert listing.title == "Test Listing"
        assert listing.price == Decimal('99.99')
        assert listing.stock == 5
        assert listing.is_active
    
    def test_listing_str_representation(self, listing):
        """Test listing __str__ method."""
        assert str(listing) == "Blue-Eyes White Dragon - Mint Condition"


@pytest.mark.django_db
class TestListingViews:
    """Test listing views."""
    
    def test_listing_detail_view(self, client, listing):
        """Test listing detail view."""
        response = client.get(f'/listing/{listing.id}/')
        assert response.status_code == 200
        assert listing.title in response.content.decode()
    
    def test_listing_create_view_requires_login(self, client):
        """Test that listing creation requires authentication."""
        response = client.get('/listings/create/')
        assert response.status_code == 302  # Redirect to login
    
    def test_listing_create_view_requires_seller_role(self, authenticated_buyer_client):
        """Test that only sellers can create listings."""
        response = authenticated_buyer_client.get('/listings/create/')
        assert response.status_code == 302  # Redirect (not authorized)

