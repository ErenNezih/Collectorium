"""
Tests for User model and authentication.
"""

import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
class TestUserModel:
    """Test User model functionality."""
    
    def test_create_user(self):
        """Test creating a regular user."""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            role='buyer'
        )
        assert user.username == 'testuser'
        assert user.email == 'test@example.com'
        assert user.role == 'buyer'
        assert user.check_password('testpass123')
        assert not user.is_staff
        assert not user.is_superuser
    
    def test_create_seller_user(self):
        """Test creating a seller user."""
        user = User.objects.create_user(
            username='seller',
            email='seller@example.com',
            password='testpass123',
            role='seller'
        )
        assert user.role == 'seller'
    
    def test_user_full_name_property(self):
        """Test full_name property."""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            first_name='John',
            last_name='Doe'
        )
        assert user.full_name == 'John Doe'
    
    def test_user_full_name_fallback(self):
        """Test full_name falls back to username."""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com'
        )
        assert user.full_name == 'testuser'

