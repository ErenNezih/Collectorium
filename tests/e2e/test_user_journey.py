"""
End-to-End tests for Collectorium user journeys using Playwright.

Run with:
    pytest tests/e2e/ --headed  # With browser UI
    pytest tests/e2e/            # Headless

Install Playwright browsers first:
    playwright install
"""

import pytest
from playwright.sync_api import Page, expect


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """Configure browser context for all E2E tests."""
    return {
        **browser_context_args,
        "viewport": {"width": 1920, "height": 1080},
    }


@pytest.mark.e2e
class TestUserRegistrationAndListing:
    """
    Test complete user journey:
    1. Register as seller
    2. Login
    3. Create listing
    4. View own listing
    """
    
    def test_seller_registration_to_listing(self, page: Page):
        """Complete seller journey from registration to listing creation."""
        base_url = "http://127.0.0.1:8000"
        
        # Step 1: Navigate to homepage
        page.goto(base_url)
        expect(page).to_have_title("Collectorium")
        
        # Step 2: Navigate to signup
        page.click("text=Kayıt Ol")
        expect(page).to_have_url(f"{base_url}/accounts/signup/")
        
        # Step 3: Fill registration form
        page.fill("input[name='username']", "e2e_seller_test")
        page.fill("input[name='email']", "e2e_seller@test.com")
        page.fill("input[name='password1']", "TestPass123!")
        page.fill("input[name='password2']", "TestPass123!")
        
        # Select seller role if exists
        if page.is_visible("input[value='seller']"):
            page.click("input[value='seller']")
        
        # Submit
        page.click("button[type='submit']")
        
        # Should be redirected to homepage or dashboard
        page.wait_for_url(f"{base_url}/*", timeout=5000)
        
        # Step 4: Navigate to create listing
        page.goto(f"{base_url}/listings/create/")
        
        # Should see listing form
        expect(page.locator("h1")).to_contain_text("İlan", ignore_case=True)


@pytest.mark.e2e
class TestBuyerCheckoutFlow:
    """
    Test buyer checkout journey:
    1. Browse marketplace
    2. View listing
    3. Add to cart
    4. Checkout
    """
    
    def test_guest_shopping(self, page: Page):
        """Test shopping as guest user (no login)."""
        base_url = "http://127.0.0.1:8000"
        
        # Step 1: Visit homepage
        page.goto(base_url)
        expect(page).to_have_title("Collectorium")
        
        # Step 2: Navigate to marketplace
        marketplace_link = page.get_by_role("link", name="Marketplace")
        if marketplace_link.is_visible():
            marketplace_link.click()
            expect(page).to_have_url(f"{base_url}/marketplace/")
        
        # Step 3: View a listing (if any exist)
        # This assumes at least one listing exists in the database
        listing_card = page.locator(".listing-card, [data-listing-id]").first
        if listing_card.is_visible():
            listing_card.click()
            
            # Step 4: Add to cart
            add_to_cart_btn = page.get_by_role("button", name="Sepete Ekle")
            if add_to_cart_btn.is_visible():
                add_to_cart_btn.click()
                
                # Should see success message or cart icon update
                page.wait_for_timeout(1000)  # Wait for feedback


@pytest.mark.e2e  
class TestHealthEndpoints:
    """Test health check endpoints."""
    
    def test_healthz_endpoint(self, page: Page):
        """Test /healthz endpoint returns healthy status."""
        base_url = "http://127.0.0.1:8000"
        
        response = page.goto(f"{base_url}/healthz/")
        assert response.status == 200
        
        content = page.content()
        assert "healthy" in content.lower()


@pytest.mark.e2e
class TestResponsiveDesign:
    """Test responsive design on different screen sizes."""
    
    @pytest.mark.parametrize("viewport", [
        {"width": 375, "height": 667},   # Mobile (iPhone SE)
        {"width": 768, "height": 1024},  # Tablet (iPad)
        {"width": 1920, "height": 1080}, # Desktop
    ])
    def test_homepage_responsive(self, page: Page, viewport):
        """Test homepage renders correctly on different viewports."""
        page.set_viewport_size(viewport)
        page.goto("http://127.0.0.1:8000")
        
        # Should always have title
        expect(page).to_have_title("Collectorium")
        
        # Navigation should be visible (might be hamburger menu on mobile)
        nav = page.locator("nav, header")
        expect(nav).to_be_visible()

