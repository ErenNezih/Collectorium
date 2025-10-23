# 🚀 cPanel Deployment Rehberi - Collectorium

## 📋 ÖN HAZIRLIK

### 1. Git Repository Path Düzeltme
**SORUN:** Git path'inde çift slash var: `/home/collecto//home/collecto/collectorium`

**ÇÖZÜM:**
1. cPanel → Git Version Control → Manage Repository
2. Repository Path'i düzelt: `/home/collecto/collectorium`
3. "Update" butonuna tıkla

### 2. Python App Konfigürasyonu
**Mevcut ayarlar:**
- Python version: 3.12.11 ✅
- Application root: collectorium ✅
- Application URL: collectorium.com.tr ✅
- Startup file: passenger_wsgi.py ✅
- Entry point: application ✅

## 🔧 ADIM ADIM DEPLOYMENT

### ADIM 1: Dependencies Yükleme (10 dakika)

**cPanel → Python App → Configuration files**

Aşağıdaki paketleri tek tek ekle:

```bash
pip install Django==5.2.1
pip install django-allauth==65.0.0
pip install django-htmx==1.26.0
pip install whitenoise==6.5.0
pip install Pillow==11.0.0
pip install mysqlclient==2.2.0
pip install PyMySQL>=1.1.0
pip install python-dotenv==1.0.0
pip install dj-database-url==3.0.0
pip install django-environ==0.11.2
pip install requests==2.31.0
pip install requests-oauthlib==2.0.0
pip install PyJWT==2.8.0
pip install google-auth==2.28.0
pip install cryptography>=42.0.0
pip install sentry-sdk==2.14.0
```

**VEYA** "Run Pip Install" butonuna tıkla ve `requirements-cpanel.txt` dosyasını yükle.

### ADIM 2: Environment Variables Ayarlama (5 dakika)

**cPanel → Python App → Environment variables**

Aşağıdaki değişkenleri ekle:

```bash
DJANGO_SETTINGS_MODULE=collectorium.settings.hosting
SECRET_KEY=8%jf93#asd!J0we0
DEBUG=False
ALLOWED_HOSTS=collectorium.com.tr,www.collectorium.com.tr
CSRF_TRUSTED_ORIGINS=https://collectorium.com.tr,https://www.collectorium.com.tr
DB_ENGINE=django.db.backends.mysql
DB_HOST=localhost
DB_NAME=collecto_collectorium
DB_USER=collecto_collecto_app
DB_PASSWORD=8%jf93#asd!J0we0
DB_PORT=3306
SECURE_SSL_REDIRECT=True
SECURE_HSTS_SECONDS=31536000
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
EMAIL_HOST=localhost
EMAIL_PORT=587
EMAIL_USE_TLS=True
DEFAULT_FROM_EMAIL=noreply@collectorium.com.tr
LOG_LEVEL=INFO
```

### ADIM 3: Database Migration (5 dakika)

**cPanel → Python App → Execute python script**

**Script 1: Migration Plan**
- Script path: `/home/collecto/collectorium/manage.py`
- Arguments: `migrate --plan`

**Script 2: Apply Migrations**
- Script path: `/home/collecto/collectorium/manage.py`
- Arguments: `migrate --noinput`

### ADIM 4: Superuser Oluşturma (5 dakika)

**cPanel → Python App → Execute python script**
- Script path: `/home/collecto/collectorium/manage.py`
- Arguments: `createsuperuser`

**VEYA** Terminal kullan:
```bash
cd /home/collecto/collectorium
source /home/collecto/virtualenv/collectorium/3.12/bin/activate
python manage.py createsuperuser
```

### ADIM 5: Static Files Collect (3 dakika)

**cPanel → Python App → Execute python script**
- Script path: `/home/collecto/collectorium/manage.py`
- Arguments: `collectstatic --noinput --clear`

### ADIM 6: Database Connection Test (2 dakika)

**cPanel → Python App → Execute python script**
- Script path: `/home/collecto/collectorium/scripts/test_db_connection.py`

### ADIM 7: Application Restart (1 dakika)

**cPanel → Python App → Restart**

## 🧪 TEST VE DOĞRULAMA

### 1. Health Check
```bash
curl https://collectorium.com.tr/healthz/
```

**Beklenen sonuç:**
```json
{
  "status": "healthy",
  "database": "connected",
  "django": "ok"
}
```

### 2. Homepage Test
```bash
curl https://collectorium.com.tr/
```

**Beklenen sonuç:** HTML sayfa içeriği

### 3. Admin Panel Test
```bash
curl https://collectorium.com.tr/admin/
```

**Beklenen sonuç:** Django admin login sayfası

### 4. Static Files Test
```bash
curl https://collectorium.com.tr/static/admin/css/base.css
```

**Beklenen sonuç:** CSS dosya içeriği

## 🚨 SORUN GİDERME

### Sorun 1: "Deploy HEAD Commit" Sonsuz Bekleme
**Neden:** Git path hatası veya eksik dependencies
**Çözüm:** 
1. Git path'i düzelt
2. Tüm dependencies'i yükle
3. Manuel deployment yap

### Sorun 2: Database Connection Error
**Neden:** MySQL credentials yanlış
**Çözüm:**
1. cPanel → MySQL Databases kontrol et
2. Environment variables'ı güncelle
3. Database connection test çalıştır

### Sorun 3: Static Files 404
**Neden:** collectstatic çalıştırılmamış
**Çözüm:**
1. `python manage.py collectstatic --noinput --clear`
2. WhiteNoise konfigürasyonunu kontrol et

### Sorun 4: 500 Internal Server Error
**Neden:** Django settings hatası
**Çözüm:**
1. Environment variables'ı kontrol et
2. Django check çalıştır: `python manage.py check --deploy`
3. Logs'u kontrol et: `/home/collecto/collectorium/logs/`

## 📞 DESTEK

**Log Dosyaları:**
- Django logs: `/home/collecto/collectorium/logs/django.log`
- Error logs: `/home/collecto/collectorium/logs/error.log`
- cPanel logs: cPanel → Error Logs

**Test Scriptleri:**
- Database test: `python scripts/test_db_connection.py`
- Smoke test: `python scripts/smoke_test.py --base-url https://collectorium.com.tr`

**Manuel Test:**
```bash
cd /home/collecto/collectorium
source /home/collecto/virtualenv/collectorium/3.12/bin/activate
python manage.py check --deploy
python manage.py runserver 0.0.0.0:8000
```

## ✅ BAŞARILI DEPLOYMENT KONTROL LİSTESİ

- [ ] Git repository path düzeltildi
- [ ] Tüm dependencies yüklendi
- [ ] Environment variables ayarlandı
- [ ] Database migration'ları çalıştırıldı
- [ ] Superuser oluşturuldu
- [ ] Static files collect edildi
- [ ] Database connection test başarılı
- [ ] Application restart edildi
- [ ] Health check endpoint çalışıyor
- [ ] Homepage erişilebilir
- [ ] Admin panel erişilebilir
- [ ] Static files serve ediliyor

**🎉 Tüm adımlar tamamlandığında siteniz canlıda olacak!**
