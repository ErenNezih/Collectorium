#!/usr/bin/env python3
"""
🚀 cPanel Deployment Fix Script
Bu script cPanel deployment sorunlarını otomatik olarak düzeltir.
"""

import os
import sys
import subprocess
from pathlib import Path

def run_command(cmd, description):
    """Komut çalıştır ve sonucu göster"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=True)
        print(f"✅ {description} başarılı")
        if result.stdout:
            print(f"📤 Output: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} başarısız")
        print(f"📤 Error: {e.stderr.strip()}")
        return False

def check_environment():
    """Environment kontrolü"""
    print("🔍 Environment kontrolü...")
    
    # Django settings module
    settings_module = os.environ.get('DJANGO_SETTINGS_MODULE', 'collectorium.settings.hosting')
    print(f"📋 DJANGO_SETTINGS_MODULE: {settings_module}")
    
    # Current directory
    current_dir = os.getcwd()
    print(f"📁 Current directory: {current_dir}")
    
    # Check if manage.py exists
    manage_py = Path('manage.py')
    if manage_py.exists():
        print("✅ manage.py bulundu")
    else:
        print("❌ manage.py bulunamadı")
        return False
    
    return True

def install_dependencies():
    """Dependencies yükle"""
    print("\n📦 Dependencies yükleniyor...")
    
    # Requirements dosyasını kontrol et
    requirements_file = Path('requirements.txt')
    if not requirements_file.exists():
        print("❌ requirements.txt bulunamadı")
        return False
    
    # Pip install
    if not run_command("pip install -r requirements.txt", "Requirements yükleme"):
        return False
    
    # Pip check
    if not run_command("pip check", "Dependencies kontrolü"):
        print("⚠️ Bazı dependency sorunları var, devam ediliyor...")
    
    return True

def run_migrations():
    """Database migration'ları çalıştır"""
    print("\n🗄️ Database migration'ları çalıştırılıyor...")
    
    # Migration plan
    if not run_command("python manage.py migrate --plan", "Migration plan"):
        return False
    
    # Apply migrations
    if not run_command("python manage.py migrate --noinput", "Migration uygulama"):
        return False
    
    return True

def collect_static_files():
    """Static files collect et"""
    print("\n📁 Static files collect ediliyor...")
    
    # Create staticfiles directory if not exists
    staticfiles_dir = Path('staticfiles')
    staticfiles_dir.mkdir(exist_ok=True)
    
    # Collect static files
    if not run_command("python manage.py collectstatic --noinput --clear", "Static files collect"):
        return False
    
    return True

def test_database_connection():
    """Database connection test"""
    print("\n🔗 Database connection test...")
    
    # Test script çalıştır
    test_script = Path('scripts/test_db_connection.py')
    if test_script.exists():
        if not run_command("python scripts/test_db_connection.py", "Database connection test"):
            return False
    else:
        print("⚠️ test_db_connection.py bulunamadı, manuel test gerekli")
    
    return True

def create_superuser():
    """Superuser oluştur (interactive)"""
    print("\n👤 Superuser oluşturma...")
    print("⚠️ Bu adım manuel olarak yapılmalı:")
    print("   python manage.py createsuperuser")
    
    return True

def main():
    """Ana fonksiyon"""
    print("🚀 cPanel Deployment Fix Başlıyor...")
    print("=" * 60)
    
    # Environment kontrolü
    if not check_environment():
        print("❌ Environment kontrolü başarısız")
        return False
    
    # Dependencies yükle
    if not install_dependencies():
        print("❌ Dependencies yükleme başarısız")
        return False
    
    # Migration'ları çalıştır
    if not run_migrations():
        print("❌ Migration'lar başarısız")
        return False
    
    # Static files collect et
    if not collect_static_files():
        print("❌ Static files collect başarısız")
        return False
    
    # Database connection test
    if not test_database_connection():
        print("❌ Database connection test başarısız")
        return False
    
    # Superuser oluştur
    create_superuser()
    
    print("\n" + "=" * 60)
    print("🎉 Deployment fix tamamlandı!")
    print("\n📋 Sonraki adımlar:")
    print("1. cPanel → Python App → Restart")
    print("2. https://collectorium.com.tr/healthz/ test et")
    print("3. Admin panel: https://collectorium.com.tr/admin/")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n❌ İşlem iptal edildi")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Beklenmeyen hata: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
