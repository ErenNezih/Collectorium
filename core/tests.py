from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class URLTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_home_page(self):
        """Ana sayfa 200 döner"""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Collectorium')

    def test_marketplace_page(self):
        """Marketplace sayfası 200 döner"""
        response = self.client.get(reverse('marketplace'))
        self.assertEqual(response.status_code, 200)

    def test_accounts_login_page(self):
        """Giriş sayfası 200 döner"""
        response = self.client.get('/accounts/login/')
        self.assertEqual(response.status_code, 200)

    def test_accounts_signup_page(self):
        """Kayıt sayfası 200 döner"""
        response = self.client.get('/accounts/signup/')
        self.assertEqual(response.status_code, 200)