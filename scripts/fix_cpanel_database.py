#!/usr/bin/env python3
"""
🔧 cPanel Database Fix Script
Environment variables'ları kontrol eder ve düzeltir
"""

import os
import sys

def check_env_vars():
    """Environment variables kontrolü"""
    print("🔍 Environment Variables Kontrolü")
    print("=" * 40)
    
    required_vars = [
        'DB_ENGINE',
        'DB_NAME', 
        'DB_USER',
        'DB_PASSWORD',
        'DB_HOST',
        'DB_PORT',
        'SECRET_KEY',
        'DJANGO_SETTINGS_MODULE'
    ]
    
    missing_vars = []
    
    for var in required_vars:
        value = os.environ.get(var)
        if value:
            # Şifreli değerleri maskele
            if 'PASSWORD' in var or 'SECRET' in var:
                display_value = value[:4] + "..." + value[-4:] if len(value) > 8 else "***"
            else:
                display_value = value
            print(f"✅ {var}: {display_value}")
        else:
            print(f"❌ {var}: EKSİK")
            missing_vars.append(var)
    
    return missing_vars

def test_database_connection():
    """Database bağlantı testi"""
    print("\n🗄️ Database Bağlantı Testi")
    print("=" * 40)
    
    try:
        # Django settings import et
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'collectorium.settings.hosting')
        
        import django
        django.setup()
        
        from django.db import connection
        
        # Bağlantı testi
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            
        if result:
            print("✅ Database bağlantısı başarılı!")
            return True
            
    except Exception as e:
        print(f"❌ Database bağlantı hatası: {e}")
        return False

def generate_env_template():
    """cPanel için env template oluştur"""
    print("\n📝 cPanel Environment Template")
    print("=" * 40)
    
    template = """
# cPanel Environment Variables
# Bu değerleri cPanel → Python → Environment Variables'a ekleyin

DB_ENGINE=mysql
DB_NAME=collecto_collectorium
DB_USER=collecto_app
DB_PASSWORD=8%jf93#asd!J0we0
DB_HOST=localhost
DB_PORT=3306
SECRET_KEY=8%jf93#asd!J0we0
DJANGO_SETTINGS_MODULE=collectorium.settings.hosting

# SSL Settings
SECURE_SSL_REDIRECT=False
SECURE_HSTS_SECONDS=31536000

# Host Settings
ALLOWED_HOSTS=collectorium.com.tr,www.collectorium.com.tr
CSRF_TRUSTED_ORIGINS=https://collectorium.com.tr,https://www.collectorium.com.tr

# Email Settings (opsiyonel)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Google OAuth (opsiyonel)
GOOGLE_CLIENT_ID=your-client-id
GOOGLE_CLIENT_SECRET=your-client-secret
"""
    
    print("📋 cPanel'e eklenecek environment variables:")
    print(template)
    
    # Dosyaya kaydet
    with open('env.cpanel.txt', 'w') as f:
        f.write(template)
    
    print("💾 Template 'env.cpanel.txt' dosyasına kaydedildi")

def main():
    """Ana fonksiyon"""
    print("🔧 cPanel Database Fix Tool")
    print("=" * 50)
    
    # 1. Environment variables kontrolü
    missing_vars = check_env_vars()
    
    # 2. Database bağlantı testi
    db_ok = test_database_connection()
    
    # 3. Template oluştur
    generate_env_template()
    
    # 4. Öneriler
    print("\n🎯 Öneriler:")
    print("=" * 40)
    
    if missing_vars:
        print("❌ Eksik environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\n📝 Çözüm:")
        print("1. cPanel → Python → Environment Variables")
        print("2. 'env.cpanel.txt' dosyasındaki değerleri ekle")
    
    if not db_ok:
        print("❌ Database bağlantı sorunu")
        print("\n📝 Çözüm:")
        print("1. MySQL database'in çalıştığını kontrol et")
        print("2. Database credentials'ları doğrula")
        print("3. 'collecto_collectorium' database'in var olduğunu kontrol et")
    
    if not missing_vars and db_ok:
        print("✅ Tüm kontroller başarılı!")
        print("🚀 Site hazır: https://collectorium.com.tr/healthz")

if __name__ == "__main__":
    main()
