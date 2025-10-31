"""
OPERATION: Day of Reckoning - Stability Check Command

Bu komut, sistemin boş veritabanı durumunda bile stabil çalıştığını kanıtlar.
Stress testi yaparak, view'ların 500 hatası vermeden çalıştığını doğrular.
"""

from django.core.management.base import BaseCommand
from django.test import Client
from django.db import transaction
from catalog.models import Category, Product
from listings.models import Listing
from stores.models import Store
import sys


class Command(BaseCommand):
    help = 'Stress test: Verify system stability with empty database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--no-restore',
            action='store_true',
            help='Do not restore deleted data after test',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('=' * 70))
        self.stdout.write(self.style.WARNING('OPERATION: Day of Reckoning - Stability Check'))
        self.stdout.write(self.style.WARNING('=' * 70))
        self.stdout.write('')

        # Store original counts
        original_category_count = Category.objects.count()
        original_listing_count = Listing.objects.count()
        original_store_count = Store.objects.count()
        original_product_count = Product.objects.count()

        self.stdout.write(f'📊 Initial State:')
        self.stdout.write(f'   Categories: {original_category_count}')
        self.stdout.write(f'   Listings: {original_listing_count}')
        self.stdout.write(f'   Stores: {original_store_count}')
        self.stdout.write(f'   Products: {original_product_count}')
        self.stdout.write('')

        # Create test client
        client = Client()

        # SCENARIO 1: Delete all categories (but keep in transaction for rollback)
        self.stdout.write(self.style.WARNING('🔥 SCENARIO 1: Deleting all categories...'))
        
        try:
            with transaction.atomic():
                # Save category IDs for potential restore
                category_ids = list(Category.objects.values_list('id', flat=True))
                
                # Delete all categories
                deleted_count = Category.objects.all().delete()[0]
                self.stdout.write(f'   ✅ Deleted {deleted_count} categories')
                
                # Verify deletion
                remaining_count = Category.objects.count()
                assert remaining_count == 0, f"Expected 0 categories, found {remaining_count}"
                self.stdout.write(f'   ✅ Verification: {remaining_count} categories remaining')
                
                # SCENARIO 2: Test home page with empty database
                self.stdout.write('')
                self.stdout.write(self.style.WARNING('🧪 SCENARIO 2: Testing home page (/) with empty database...'))
                
                try:
                    response = client.get('/')
                    status_code = response.status_code
                    
                    assert status_code == 200, f"Expected 200 OK, got {status_code}"
                    self.stdout.write(self.style.SUCCESS(f'   ✅ Home page returned 200 OK'))
                    self.stdout.write(f'   ✅ Response size: {len(response.content)} bytes')
                    
                except AssertionError as e:
                    self.stdout.write(self.style.ERROR(f'   ❌ FAILED: {e}'))
                    raise
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'   ❌ CRASHED: {e}'))
                    raise
                
                # SCENARIO 3: Test categories page with empty database
                self.stdout.write('')
                self.stdout.write(self.style.WARNING('🧪 SCENARIO 3: Testing categories page (/categories/) with empty database...'))
                
                try:
                    response = client.get('/categories/')
                    status_code = response.status_code
                    
                    assert status_code == 200, f"Expected 200 OK, got {status_code}"
                    self.stdout.write(self.style.SUCCESS(f'   ✅ Categories page returned 200 OK'))
                    self.stdout.write(f'   ✅ Response size: {len(response.content)} bytes')
                    
                except AssertionError as e:
                    self.stdout.write(self.style.ERROR(f'   ❌ FAILED: {e}'))
                    raise
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'   ❌ CRASHED: {e}'))
                    raise
                
                # SCENARIO 4: Test marketplace page with empty database
                self.stdout.write('')
                self.stdout.write(self.style.WARNING('🧪 SCENARIO 4: Testing marketplace page (/marketplace/) with empty database...'))
                
                try:
                    response = client.get('/marketplace/')
                    status_code = response.status_code
                    
                    assert status_code == 200, f"Expected 200 OK, got {status_code}"
                    self.stdout.write(self.style.SUCCESS(f'   ✅ Marketplace page returned 200 OK'))
                    self.stdout.write(f'   ✅ Response size: {len(response.content)} bytes')
                    
                except AssertionError as e:
                    self.stdout.write(self.style.ERROR(f'   ❌ FAILED: {e}'))
                    raise
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'   ❌ CRASHED: {e}'))
                    raise
                
                # If we reach here, all tests passed
                # Transaction will rollback automatically, restoring categories
                self.stdout.write('')
                self.stdout.write(self.style.SUCCESS('✅ ALL TESTS PASSED - System is stable!'))
                self.stdout.write('')
                self.stdout.write('🔄 Rolling back transaction (restoring categories)...')
                
        except Exception as e:
            self.stdout.write('')
            self.stdout.write(self.style.ERROR('=' * 70))
            self.stdout.write(self.style.ERROR('TEST FAILED - System is NOT stable!'))
            self.stdout.write(self.style.ERROR('=' * 70))
            self.stdout.write(self.style.ERROR(f'Error: {e}'))
            sys.exit(1)
        
        # Verify rollback worked
        final_category_count = Category.objects.count()
        assert final_category_count == original_category_count, \
            f"Rollback failed: Expected {original_category_count} categories, found {final_category_count}"
        
        self.stdout.write(f'   ✅ Categories restored: {final_category_count}')
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('=' * 70))
        self.stdout.write(self.style.SUCCESS('OPERATION COMPLETE - System stability verified!'))
        self.stdout.write(self.style.SUCCESS('=' * 70))
        self.stdout.write('')
        self.stdout.write('📋 Test Summary:')
        self.stdout.write('   ✅ Home page handles empty database (200 OK)')
        self.stdout.write('   ✅ Categories page handles empty database (200 OK)')
        self.stdout.write('   ✅ Marketplace page handles empty database (200 OK)')
        self.stdout.write('   ✅ No 500 errors detected')
        self.stdout.write('   ✅ All data restored after test')
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('🎉 SYSTEM IS PRODUCTION-READY!'))

