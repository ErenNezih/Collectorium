#!/usr/bin/env python
"""
Database Connection Test Script

Tests database connectivity and basic operations for Collectorium.
Works with both PostgreSQL and MySQL databases.

Usage:
    python scripts/test_db_connection.py
"""

import os
import sys
import django

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
from django.core.management import call_command


def test_database_connection():
    """Test basic database connectivity"""
    print("=" * 60)
    print("DATABASE CONNECTION TEST")
    print("=" * 60)
    
    # Get database config
    db_config = settings.DATABASES['default']
    db_engine = db_config['ENGINE']
    db_name = db_config.get('NAME', 'N/A')
    db_host = db_config.get('HOST', 'N/A')
    db_port = db_config.get('PORT', 'N/A')
    
    print(f"\nDatabase Configuration:")
    print(f"  Engine: {db_engine}")
    print(f"  Name: {db_name}")
    print(f"  Host: {db_host}")
    print(f"  Port: {db_port}")
    print()
    
    # Test connection
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            
            if result == (1,) or result == [1]:
                print("✅ Database connection: SUCCESS")
            else:
                print(f"❌ Database connection: UNEXPECTED RESULT ({result})")
                return False
    except Exception as e:
        print(f"❌ Database connection: FAILED")
        print(f"   Error: {e}")
        return False
    
    # Get database version
    try:
        with connection.cursor() as cursor:
            if 'postgresql' in db_engine:
                cursor.execute("SELECT version()")
                version = cursor.fetchone()[0]
                print(f"✅ PostgreSQL version: {version.split(',')[0]}")
            elif 'mysql' in db_engine:
                cursor.execute("SELECT VERSION()")
                version = cursor.fetchone()[0]
                print(f"✅ MySQL version: {version}")
            else:
                print("ℹ️  Database version: Unknown engine")
    except Exception as e:
        print(f"⚠️  Could not retrieve database version: {e}")
    
    # Test database write/read
    print("\nTesting write/read operations...")
    try:
        with connection.cursor() as cursor:
            # Create temporary test table
            cursor.execute("""
                CREATE TEMPORARY TABLE test_connection_table (
                    id INTEGER PRIMARY KEY,
                    test_value VARCHAR(100)
                )
            """)
            
            # Insert test data
            cursor.execute("""
                INSERT INTO test_connection_table (id, test_value)
                VALUES (1, 'test_data')
            """)
            
            # Read test data
            cursor.execute("SELECT test_value FROM test_connection_table WHERE id = 1")
            result = cursor.fetchone()[0]
            
            if result == 'test_data':
                print("✅ Write/Read operations: SUCCESS")
            else:
                print(f"❌ Write/Read operations: FAILED (got: {result})")
                return False
    except Exception as e:
        print(f"❌ Write/Read operations: FAILED")
        print(f"   Error: {e}")
        return False
    
    # Check migrations status
    print("\nChecking migrations status...")
    try:
        # Get list of unapplied migrations
        from django.db.migrations.executor import MigrationExecutor
        executor = MigrationExecutor(connection)
        plan = executor.migration_plan(executor.loader.graph.leaf_nodes())
        
        if plan:
            print(f"⚠️  Unapplied migrations: {len(plan)}")
            print("   Run: python manage.py migrate")
        else:
            print("✅ All migrations applied")
    except Exception as e:
        print(f"⚠️  Could not check migrations: {e}")
    
    # Check if tables exist
    print("\nChecking core tables...")
    try:
        with connection.cursor() as cursor:
            # Check for key tables
            core_tables = ['auth_user', 'accounts_user', 'listings_listing']
            
            for table in core_tables:
                try:
                    cursor.execute(f"SELECT COUNT(*) FROM {table}")
                    count = cursor.fetchone()[0]
                    print(f"✅ Table '{table}': {count} rows")
                except Exception:
                    print(f"⚠️  Table '{table}': Not found (run migrations)")
    except Exception as e:
        print(f"⚠️  Could not check tables: {e}")
    
    return True


def main():
    """Main function"""
    try:
        success = test_database_connection()
        
        print("\n" + "=" * 60)
        if success:
            print("DATABASE TEST: ✅ PASSED")
        else:
            print("DATABASE TEST: ❌ FAILED")
        print("=" * 60)
        
        sys.exit(0 if success else 1)
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()


