#!/usr/bin/env python
"""
Comprehensive Smoke Test for Collectorium cPanel Deployment

Tests all critical functionality to verify deployment health.

Usage:
    python scripts/smoke_test.py [--base-url https://yourdomain.com]
"""

import os
import sys
import django
import argparse
import requests
from urllib.parse import urljoin

# Add project directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'collectorium.settings.hosting')

try:
    django.setup()
except Exception as e:
    print(f"❌ Failed to initialize Django: {e}")
    sys.exit(1)

from django.db import connection
from django.conf import settings


class Colors:
    """ANSI color codes"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


def print_header(text):
    """Print section header"""
    print(f"\n{Colors.CYAN}{Colors.BOLD}{'='*60}{Colors.RESET}")
    print(f"{Colors.CYAN}{Colors.BOLD}{text}{Colors.RESET}")
    print(f"{Colors.CYAN}{Colors.BOLD}{'='*60}{Colors.RESET}\n")


def print_test(name):
    """Print test name"""
    print(f"{Colors.BLUE}Testing:{Colors.RESET} {name}...", end=" ")


def print_pass(message="PASS"):
    """Print pass message"""
    print(f"{Colors.GREEN}✅ {message}{Colors.RESET}")


def print_fail(message="FAIL"):
    """Print fail message"""
    print(f"{Colors.RED}❌ {message}{Colors.RESET}")


def print_warn(message):
    """Print warning message"""
    print(f"{Colors.YELLOW}⚠️  {message}{Colors.RESET}")


class SmokeTest:
    """Smoke test suite"""
    
    def __init__(self, base_url=None):
        self.base_url = base_url or 'http://localhost:8000'
        self.tests_passed = 0
        self.tests_failed = 0
        self.tests_warned = 0
    
    def run_all(self):
        """Run all smoke tests"""
        print_header("COLLECTORIUM SMOKE TEST SUITE")
        print(f"Base URL: {self.base_url}")
        print(f"Settings: {settings.SETTINGS_MODULE}")
        
        # Django Tests
        self.test_django_settings()
        self.test_database()
        
        # HTTP Tests (if base_url is accessible)
        if self.base_url != 'http://localhost:8000' or self._is_server_running():
            self.test_health_endpoint()
            self.test_homepage()
            self.test_admin_page()
            self.test_static_files()
        else:
            print_warn("Server not running - skipping HTTP tests")
        
        # Summary
        self.print_summary()
    
    def _is_server_running(self):
        """Check if development server is running"""
        try:
            response = requests.get(self.base_url, timeout=2)
            return True
        except:
            return False
    
    def test_django_settings(self):
        """Test Django settings configuration"""
        print_header("DJANGO SETTINGS")
        
        # DEBUG setting
        print_test("DEBUG setting")
        if settings.DEBUG is False:
            print_pass("DEBUG=False (production)")
            self.tests_passed += 1
        else:
            print_warn("DEBUG=True (should be False in production)")
            self.tests_warned += 1
        
        # SECRET_KEY
        print_test("SECRET_KEY")
        if settings.SECRET_KEY and len(settings.SECRET_KEY) > 30:
            print_pass("Strong SECRET_KEY configured")
            self.tests_passed += 1
        else:
            print_fail("Weak or missing SECRET_KEY")
            self.tests_failed += 1
        
        # ALLOWED_HOSTS
        print_test("ALLOWED_HOSTS")
        if settings.ALLOWED_HOSTS and settings.ALLOWED_HOSTS != ['']:
            print_pass(f"Configured: {', '.join(settings.ALLOWED_HOSTS[:3])}")
            self.tests_passed += 1
        else:
            print_fail("ALLOWED_HOSTS not configured")
            self.tests_failed += 1
        
        # CSRF_TRUSTED_ORIGINS
        print_test("CSRF_TRUSTED_ORIGINS")
        if hasattr(settings, 'CSRF_TRUSTED_ORIGINS') and settings.CSRF_TRUSTED_ORIGINS:
            print_pass(f"Configured: {len(settings.CSRF_TRUSTED_ORIGINS)} origin(s)")
            self.tests_passed += 1
        else:
            print_fail("CSRF_TRUSTED_ORIGINS not configured")
            self.tests_failed += 1
        
        # Security headers
        print_test("Security headers")
        security_ok = all([
            settings.SECURE_SSL_REDIRECT,
            settings.SECURE_HSTS_SECONDS > 0,
            settings.SESSION_COOKIE_SECURE,
            settings.CSRF_COOKIE_SECURE,
        ])
        if security_ok:
            print_pass("All security headers configured")
            self.tests_passed += 1
        else:
            print_warn("Some security headers not configured")
            self.tests_warned += 1
        
        # Static files
        print_test("Static files configuration")
        if settings.STATIC_ROOT and os.path.exists(settings.STATIC_ROOT):
            static_count = sum([len(files) for r, d, files in os.walk(settings.STATIC_ROOT)])
            print_pass(f"Static root exists ({static_count} files)")
            self.tests_passed += 1
        else:
            print_warn(f"Static root not found: {settings.STATIC_ROOT}")
            self.tests_warned += 1
    
    def test_database(self):
        """Test database connectivity and configuration"""
        print_header("DATABASE")
        
        db_config = settings.DATABASES['default']
        
        # Database engine
        print_test("Database engine")
        db_engine = db_config['ENGINE']
        if 'postgresql' in db_engine or 'mysql' in db_engine:
            engine_name = 'PostgreSQL' if 'postgresql' in db_engine else 'MySQL'
            print_pass(f"{engine_name} configured")
            self.tests_passed += 1
        else:
            print_warn(f"Using {db_engine}")
            self.tests_warned += 1
        
        # Connection test
        print_test("Database connection")
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                result = cursor.fetchone()
                if result:
                    print_pass("Connection successful")
                    self.tests_passed += 1
                else:
                    print_fail("Unexpected result")
                    self.tests_failed += 1
        except Exception as e:
            print_fail(f"Connection failed: {e}")
            self.tests_failed += 1
        
        # Tables check
        print_test("Database tables")
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM auth_user")
                user_count = cursor.fetchone()[0]
                print_pass(f"{user_count} user(s) in database")
                self.tests_passed += 1
        except Exception as e:
            print_warn(f"Tables may not exist: {e}")
            self.tests_warned += 1
        
        # Migrations check
        print_test("Database migrations")
        try:
            from django.db.migrations.executor import MigrationExecutor
            executor = MigrationExecutor(connection)
            plan = executor.migration_plan(executor.loader.graph.leaf_nodes())
            
            if not plan:
                print_pass("All migrations applied")
                self.tests_passed += 1
            else:
                print_warn(f"{len(plan)} unapplied migration(s)")
                self.tests_warned += 1
        except Exception as e:
            print_warn(f"Could not check migrations: {e}")
            self.tests_warned += 1
    
    def test_health_endpoint(self):
        """Test health check endpoint"""
        print_header("HEALTH CHECK ENDPOINT")
        
        health_url = urljoin(self.base_url, '/healthz/')
        
        print_test("Health endpoint")
        try:
            response = requests.get(health_url, timeout=10)
            
            if response.status_code == 200:
                print_pass(f"Status 200 OK")
                self.tests_passed += 1
                
                # Check JSON response
                try:
                    data = response.json()
                    
                    print_test("Health response format")
                    if 'status' in data and 'database' in data:
                        print_pass("Valid JSON format")
                        self.tests_passed += 1
                        
                        print(f"  Status: {data.get('status')}")
                        print(f"  Database: {data.get('database')}")
                        print(f"  Django: {data.get('django')}")
                    else:
                        print_warn("Missing expected fields")
                        self.tests_warned += 1
                        
                except Exception as e:
                    print_warn(f"Invalid JSON: {e}")
                    self.tests_warned += 1
            else:
                print_fail(f"Status {response.status_code}")
                self.tests_failed += 1
                
        except requests.exceptions.RequestException as e:
            print_fail(f"Request failed: {e}")
            self.tests_failed += 1
    
    def test_homepage(self):
        """Test homepage accessibility"""
        print_header("HOMEPAGE")
        
        print_test("Homepage GET")
        try:
            response = requests.get(self.base_url, timeout=10)
            
            if response.status_code == 200:
                print_pass("Status 200 OK")
                self.tests_passed += 1
                
                # Check content
                if 'Collectorium' in response.text or 'collectorium' in response.text.lower():
                    print_pass("Homepage content looks valid")
                    self.tests_passed += 1
                else:
                    print_warn("Homepage content unexpected")
                    self.tests_warned += 1
            else:
                print_fail(f"Status {response.status_code}")
                self.tests_failed += 1
                
        except requests.exceptions.RequestException as e:
            print_fail(f"Request failed: {e}")
            self.tests_failed += 1
    
    def test_admin_page(self):
        """Test admin page accessibility"""
        print_header("ADMIN PAGE")
        
        admin_url = urljoin(self.base_url, '/admin/')
        
        print_test("Admin page GET")
        try:
            response = requests.get(admin_url, timeout=10, allow_redirects=True)
            
            if response.status_code == 200:
                print_pass("Status 200 OK")
                self.tests_passed += 1
                
                # Check for Django admin indicators
                if 'Django' in response.text and ('username' in response.text.lower() or 'password' in response.text.lower()):
                    print_pass("Admin login page loads correctly")
                    self.tests_passed += 1
                else:
                    print_warn("Admin page content unexpected")
                    self.tests_warned += 1
            else:
                print_fail(f"Status {response.status_code}")
                self.tests_failed += 1
                
        except requests.exceptions.RequestException as e:
            print_fail(f"Request failed: {e}")
            self.tests_failed += 1
    
    def test_static_files(self):
        """Test static files serving"""
        print_header("STATIC FILES")
        
        # Test common static file
        static_url = urljoin(self.base_url, '/static/admin/css/base.css')
        
        print_test("Static file serving")
        try:
            response = requests.head(static_url, timeout=10)
            
            if response.status_code == 200:
                print_pass("Static files accessible")
                self.tests_passed += 1
            elif response.status_code == 404:
                print_warn("Static files not found (run collectstatic)")
                self.tests_warned += 1
            else:
                print_fail(f"Status {response.status_code}")
                self.tests_failed += 1
                
        except requests.exceptions.RequestException as e:
            print_warn(f"Could not test static files: {e}")
            self.tests_warned += 1
    
    def print_summary(self):
        """Print test summary"""
        print_header("TEST SUMMARY")
        
        total_tests = self.tests_passed + self.tests_failed + self.tests_warned
        
        print(f"{Colors.GREEN}✅ Passed: {self.tests_passed}{Colors.RESET}")
        print(f"{Colors.RED}❌ Failed: {self.tests_failed}{Colors.RESET}")
        print(f"{Colors.YELLOW}⚠️  Warnings: {self.tests_warned}{Colors.RESET}")
        print(f"{Colors.BOLD}📊 Total: {total_tests}{Colors.RESET}")
        print()
        
        if self.tests_failed == 0:
            if self.tests_warned == 0:
                print(f"{Colors.GREEN}{Colors.BOLD}🎉 ALL TESTS PASSED!{Colors.RESET}")
                return True
            else:
                print(f"{Colors.YELLOW}{Colors.BOLD}✅ TESTS PASSED (with warnings){Colors.RESET}")
                return True
        else:
            print(f"{Colors.RED}{Colors.BOLD}❌ SOME TESTS FAILED{Colors.RESET}")
            return False


def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='Run smoke tests for Collectorium')
    parser.add_argument(
        '--base-url',
        help='Base URL of the application (default: http://localhost:8000)',
        default='http://localhost:8000'
    )
    args = parser.parse_args()
    
    try:
        smoke_test = SmokeTest(base_url=args.base_url)
        success = smoke_test.run_all()
        
        sys.exit(0 if success else 1)
        
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}⚠️  Test interrupted by user{Colors.RESET}")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n{Colors.RED}❌ Unexpected error: {e}{Colors.RESET}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()


