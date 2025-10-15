"""
Tests for Store model and views.
"""

import pytest
from stores.models import Store


@pytest.mark.django_db
class TestStoreModel:
    """Test Store model functionality."""
    
    def test_create_store(self, seller_user):
        """Test creating a store."""
        store = Store.objects.create(
            owner=seller_user,
            name="My Store",
            slug="my-store",
            bio="Welcome to my store"
        )
        assert store.owner == seller_user
        assert store.name == "My Store"
        assert not store.is_verified
    
    def test_store_str_representation(self, store):
        """Test store __str__ method."""
        assert str(store) == "Test Store"


@pytest.mark.django_db
class TestStoreViews:
    """Test store views."""
    
    def test_stores_list_view(self, client, store):
        """Test stores list view."""
        response = client.get('/stores/')
        assert response.status_code == 200
        assert 'Test Store' in response.content.decode()
    
    def test_store_detail_view(self, client, store):
        """Test store detail view."""
        response = client.get(f'/stores/{store.slug}/')
        assert response.status_code == 200
        assert store.name in response.content.decode()

