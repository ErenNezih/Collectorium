"""
Locust load testing scenarios for Collectorium.

Run with:
    locust -f tests/load/locustfile.py --host=http://127.0.0.1:8000
    
Then open http://localhost:8089 to configure and start the test.
"""

from locust import HttpUser, task, between
import random


class BuyerUser(HttpUser):
    """
    Simulates a buyer browsing the marketplace.
    
    Weight: 7 (70% of users are buyers)
    """
    
    weight = 7
    wait_time = between(2, 5)  # Wait 2-5 seconds between tasks
    
    def on_start(self):
        """Called when a user starts."""
        # Visit homepage first
        self.client.get("/")
    
    @task(5)
    def browse_homepage(self):
        """Browse homepage - most common action."""
        self.client.get("/")
    
    @task(3)
    def browse_marketplace(self):
        """Browse marketplace listings."""
        self.client.get("/marketplace/")
    
    @task(2)
    def view_listing(self):
        """View a random listing detail."""
        # Assume listing IDs from 1-20 exist
        listing_id = random.randint(1, 20)
        self.client.get(f"/listing/{listing_id}/", name="/listing/[id]/")
    
    @task(1)
    def view_stores(self):
        """View stores list."""
        self.client.get("/stores/")
    
    @task(1)
    def add_to_cart(self):
        """Attempt to add item to cart."""
        listing_id = random.randint(1, 20)
        self.client.post(
            f"/cart/add/{listing_id}/",
            {"quantity": 1, "override": False},
            name="/cart/add/[id]/"
        )


class SellerUser(HttpUser):
    """
    Simulates a seller managing their listings.
    
    Weight: 2 (20% of users are sellers)
    """
    
    weight = 2
    wait_time = between(3, 8)  # Sellers take more time
    
    @task(3)
    def view_my_listings(self):
        """View own listings (requires auth)."""
        # This will redirect to login for non-authenticated users
        self.client.get("/account/my-listings/")
    
    @task(1)
    def create_listing(self):
        """Attempt to create a listing (requires auth)."""
        self.client.get("/listings/create/")


class AnonymousVisitor(HttpUser):
    """
    Simulates anonymous visitors just browsing.
    
    Weight: 1 (10% are just browsing)
    """
    
    weight = 1
    wait_time = between(1, 3)  # Quick browsing
    
    @task(10)
    def browse(self):
        """Quick browsing of different pages."""
        pages = [
            "/",
            "/marketplace/",
            "/stores/",
            "/hakkimizda/",
        ]
        self.client.get(random.choice(pages))


class StressTest(HttpUser):
    """
    Heavy load test - simulates peak traffic.
    
    This user type is disabled by default (weight=0).
    Enable by setting weight > 0 when testing capacity.
    """
    
    weight = 0  # Disabled by default
    wait_time = between(0.5, 1)  # Very fast requests
    
    @task
    def rapid_fire(self):
        """Rapid requests to test server limits."""
        endpoints = ["/", "/healthz/", "/marketplace/"]
        self.client.get(random.choice(endpoints))

