#!/usr/bin/env python3
"""
🧪 cPanel Deployment Test Script
Bu script deployment'ın başarılı olup olmadığını test eder.
"""

import os
import sys
import requests
import subprocess
from pathlib import Path

def test_environment():
    """Environment test"""
    print("🔍 Environment Test...")
    
    # Django settings module
    settings_module = os.environ.get('DJANGO_SETTINGS_MODULE', 'collectorium.settings.hosting')
    print(f"✅ DJANGO_SETTINGS_MODULE: {settings_module}")
    
    # Current directory
    current_dir = os.getcwd()
    print(f"✅ Current directory: {current_dir}")
    
    # Check manage.py
    if Path('manage.py').exists():
        print("✅ manage.py exists")
    else:
        print("❌ manage.py not found")
        return False
    
    return True

def test_dependencies():
    """Dependencies test"""
    print("\n📦 Dependencies Test...")
    
    try:
        import django
        print(f"✅ Django {django.get_version()}")
    except ImportError:
        print("❌ Django not installed")
        return False
    
    try:
        import allauth
        print("✅ django-allauth installed")
    except ImportError:
        print("❌ django-allauth not installed")
        return False
    
    try:
        import whitenoise
        print("✅ whitenoise installed")
    except ImportError:
        print("❌ whitenoise not installed")
        return False
    
    try:
        import PIL
        print("✅ Pillow installed")
    except ImportError:
        print("❌ Pillow not installed")
        return False
    
    try:
        import pymysql
        print("✅ PyMySQL installed")
    except ImportError:
        print("❌ PyMySQL not installed")
        return False
    
    return True

def test_django_setup():
    """Django setup test"""
    print("\n🐍 Django Setup Test...")
    
    try:
        # Set Django settings
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'collectorium.settings.hosting')
        
        import django
        django.setup()
        print("✅ Django setup successful")
        
        # Test Django check
        from django.core.management import call_command
        from io import StringIO
        
        output = StringIO()
        call_command('check', stdout=output)
        print("✅ Django check passed")
        
        return True
    except Exception as e:
        print(f"❌ Django setup failed: {e}")
        return False

def test_database():
    """Database test"""
    print("\n🗄️ Database Test...")
    
    try:
        from django.db import connection
        
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            if result:
                print("✅ Database connection successful")
                return True
            else:
                print("❌ Database connection failed")
                return False
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        return False

def test_migrations():
    """Migrations test"""
    print("\n🔄 Migrations Test...")
    
    try:
        from django.db.migrations.executor import MigrationExecutor
        from django.db import connection
        
        executor = MigrationExecutor(connection)
        plan = executor.migration_plan(executor.loader.graph.leaf_nodes())
        
        if not plan:
            print("✅ All migrations applied")
            return True
        else:
            print(f"⚠️ {len(plan)} unapplied migrations")
            return False
    except Exception as e:
        print(f"❌ Migrations test failed: {e}")
        return False

def test_static_files():
    """Static files test"""
    print("\n📁 Static Files Test...")
    
    staticfiles_dir = Path('staticfiles')
    if staticfiles_dir.exists() and any(staticfiles_dir.iterdir()):
        print("✅ Static files directory exists and not empty")
        return True
    else:
        print("❌ Static files directory missing or empty")
        return False

def test_http_endpoints(base_url="https://collectorium.com.tr"):
    """HTTP endpoints test"""
    print(f"\n🌐 HTTP Endpoints Test ({base_url})...")
    
    endpoints = [
        ("/", "Homepage"),
        ("/healthz/", "Health Check"),
        ("/admin/", "Admin Panel"),
        ("/static/admin/css/base.css", "Static Files"),
    ]
    
    results = []
    
    for endpoint, name in endpoints:
        try:
            url = base_url + endpoint
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                print(f"✅ {name}: {response.status_code}")
                results.append(True)
            else:
                print(f"⚠️ {name}: {response.status_code}")
                results.append(False)
        except requests.exceptions.RequestException as e:
            print(f"❌ {name}: Connection failed - {e}")
            results.append(False)
    
    return all(results)

def run_management_command(command):
    """Run Django management command"""
    try:
        result = subprocess.run(
            ["python", "manage.py"] + command.split(),
            capture_output=True,
            text=True,
            check=True
        )
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stderr

def main():
    """Main test function"""
    print("🧪 cPanel Deployment Test Başlıyor...")
    print("=" * 60)
    
    tests = [
        ("Environment", test_environment),
        ("Dependencies", test_dependencies),
        ("Django Setup", test_django_setup),
        ("Database", test_database),
        ("Migrations", test_migrations),
        ("Static Files", test_static_files),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results.append((test_name, False))
    
    # HTTP tests (optional)
    print("\n🌐 HTTP Tests (Optional)...")
    try:
        http_result = test_http_endpoints()
        results.append(("HTTP Endpoints", http_result))
    except Exception as e:
        print(f"⚠️ HTTP tests skipped: {e}")
        results.append(("HTTP Endpoints", None))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    passed = 0
    failed = 0
    skipped = 0
    
    for test_name, result in results:
        if result is True:
            print(f"✅ {test_name}: PASSED")
            passed += 1
        elif result is False:
            print(f"❌ {test_name}: FAILED")
            failed += 1
        else:
            print(f"⚠️ {test_name}: SKIPPED")
            skipped += 1
    
    print(f"\n📈 Results: {passed} passed, {failed} failed, {skipped} skipped")
    
    if failed == 0:
        print("\n🎉 ALL TESTS PASSED! Deployment successful!")
        return True
    else:
        print(f"\n❌ {failed} test(s) failed. Check the issues above.")
        return False

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n❌ Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
