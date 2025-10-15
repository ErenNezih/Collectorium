"""
Tests for health check endpoints.
"""

import pytest
from django.urls import reverse


@pytest.mark.django_db
class TestHealthEndpoints:
    """Test health check endpoints."""
    
    def test_healthz_endpoint(self, client):
        """Test basic health check."""
        response = client.get('/healthz/')
        assert response.status_code == 200
        data = response.json()
        assert data['status'] == 'healthy'
    
    def test_readiness_endpoint(self, client):
        """Test readiness probe."""
        response = client.get('/health/readiness/')
        assert response.status_code == 200
        data = response.json()
        assert data['status'] in ['ready', 'not_ready']
        assert 'checks' in data
        assert 'database' in data['checks']
    
    def test_liveness_endpoint(self, client):
        """Test liveness probe."""
        response = client.get('/health/liveness/')
        assert response.status_code == 200
        data = response.json()
        assert data['status'] == 'alive'

