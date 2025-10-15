# 🚀 COLLECTORIUM - PYTHONANYWHERE DEPLOYMENT GUIDE

**Adım adım, copy-paste yaparak 15 dakikada deploy edin!**

---

## 📋 ÖN HAZIRLIK (Şu an yaptığınız)

✅ PythonAnywhere hesabı açtınız  
✅ Dashboard'dasınız  
✅ Username: `erennezih` (veya kendiniz)

---

## 🎯 ADIM 1: BASH CONSOLE AÇIN

1. Dashboard'da **"$ Bash"** butonuna tıklayın (sol altta, mavi)
2. Yeni bir terminal penceresi açılacak

---

## 📦 ADIM 2: PROJEYİ YÜKLEYİN

Bash console'da şu komutları **sırayla** çalıştırın:

### Option A: GitHub'dan (Eğer projeniz GitHub'daysa)

```bash
git clone https://github.com/YOURUSERNAME/Collectorium.git
cd Collectorium
```

### Option B: Dosyaları Manuel Yükle (Projeniz lokal ise)

1. **Projenizi ZIP'leyin** (tüm Collectorium klasörünü)
2. PythonAnywhere'de **"Files"** tab'ına gidin
3. **"Upload a file"** → ZIP dosyanızı yükleyin
4. Bash console'a dönün ve:

```bash
unzip Collectorium.zip
cd Collectorium
```

---

## 🐍 ADIM 3: VIRTUAL ENVIRONMENT OLUŞTUR

Bash'te:

```bash
mkvirtualenv collectorium-env --python=python3.11
```

Şimdi `(collectorium-env)` prefix'i göreceksiniz. Bu normal!

---

## 📚 ADIM 4: DEPENDENCIES YÜKLE

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**VEYA** eğer `pyproject.toml` kullanıyorsanız:

```bash
pip install -e .
```

**Ekstra gerekli paketler:**

```bash
pip install mysqlclient python-dotenv dj-database-url
```

⏳ **Bekleme süresi:** 2-3 dakika (dependency install)

---

## 🗄️ ADIM 5: MYSQL DATABASE OLUŞTUR

1. **"Databases"** tab'ına gidin (üstteki menüden)
2. **"Initialize MySQL"** → Şifre belirleyin
3. **"Create database"** → Database adı: `collectorium` (veya istediğiniz)
4. **Database bilgilerini not alın:**
   - Database name: `erennezih$collectorium`
   - Username: `erennezih`
   - Password: (az önce belirlediğiniz)
   - Hostname: `erennezih.mysql.pythonanywhere-services.com`

---

## ⚙️ ADIM 6: ENVIRONMENT VARIABLES AYARLA

Bash'te `.env.pythonanywhere` dosyasını düzenleyin:

```bash
nano .env.pythonanywhere
```

**ŞU SATIRLARI GÜNCELLEY İN:**

```bash
# SECRET_KEY oluştur (başka bir Bash tab'ında):
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
# Çıkan değeri SECRET_KEY= satırına yapıştırın

# Database bilgilerini yazın:
DB_NAME=erennezih$collectorium
DB_USER=erennezih
DB_PASSWORD=your-mysql-password
DB_HOST=erennezih.mysql.pythonanywhere-services.com

# Allowed hosts:
ALLOWED_HOSTS=erennezih.pythonanywhere.com,127.0.0.1
```

**Kaydet:** `CTRL+O` → Enter → `CTRL+X`

---

## 📁 ADIM 7: STATIC FILES COLLECT

```bash
export DJANGO_SETTINGS_MODULE=collectorium.settings.pythonanywhere
python manage.py collectstatic --noinput
```

---

## 🔄 ADIM 8: DATABASE MIGRATE

```bash
python manage.py migrate
```

---

## 👤 ADIM 9: SUPERUSER OLUŞTUR

```bash
python manage.py createsuperuser
```

- Username: `admin` (veya istediğiniz)
- Email: (isteğe bağlı)
- Password: ****

---

## 🌐 ADIM 10: WEB APP KURULUMU

1. **"Web"** tab'ına gidin (üstteki menüden)
2. **"Add a new web app"** butonuna tıklayın
3. **Domain seçin:** `erennezih.pythonanywhere.com` (otomatik gelir)
4. **"Next"**
5. **"Manual configuration"** seçin (Django seçmeyin!)
6. **Python version:** `Python 3.11`
7. **"Next"** → Web app oluşturuldu!

---

## 🔧 ADIM 11: WEB APP AYARLARI

Web tab'ında aşağıdaki bölümleri doldurun:

### A) **Code Section:**

**Source code:**
```
/home/erennezih/Collectorium
```

**Working directory:**
```
/home/erennezih/Collectorium
```

### B) **Virtualenv Section:**

```
/home/erennezih/.virtualenvs/collectorium-env
```

### C) **WSGI Configuration File:**

1. **WSGI file** linkine tıklayın (mavi link)
2. **TÜM İÇERİĞİ SİLİN**
3. Projenizde `pythonanywhere_wsgi.py` dosyasını açın
4. İçeriği **KOPYALAYIN** ve WSGI file'a **YAPIŞTIRIN**
5. **`PYTHONANYWHERE_USERNAME = 'erennezih'`** satırını kendi username'inize göre güncelleyin
6. **Save** (sağ üstte, yeşil buton)

### D) **Static Files Mapping:**

| URL | Directory |
|-----|-----------|
| `/static/` | `/home/erennezih/Collectorium/staticfiles` |
| `/media/` | `/home/erennezih/Collectorium/media` |

**"Enter URL"** ve **"Enter path"** bölümlerine yukarıdaki değerleri girin, "✓" tıklayın.

---

## 🔄 ADIM 12: RELOAD WEB APP

Web tab'ında, **yeşil "Reload" butonu**na tıklayın (sağ üstte, erennezih.pythonanywhere.com yazısının yanında)

⏳ **Bekleme:** 10-15 saniye

---

## 🎉 ADIM 13: TEST EDİN!

Tarayıcıda açın:

### Ana Sayfa:
```
https://erennezih.pythonanywhere.com
```

### Admin Panel:
```
https://erennezih.pythonanywhere.com/admin
```

**Superuser** ile giriş yapın!

---

## ❓ SORUN GİDERME

### 1) **"Something went wrong"** hatası:

**Error log** kontrol edin (Web tab → Log files → Error log)

**Sık hatalar:**

**a) Import Error:**
```bash
# Bash'te:
workon collectorium-env
pip install missing-package-name
```

**b) Database connection error:**

`.env.pythonanywhere` dosyasındaki DB bilgilerini kontrol edin

**c) Static files yüklenmiyor:**

```bash
python manage.py collectstatic --noinput
```

### 2) **CSS/JS çalışmıyor:**

Web tab → Static files mapping kontrol edin.

### 3) **500 Internal Server Error:**

Error log'a bakın:
```
# Bash'te:
tail -f /var/log/erennezih.pythonanywhere.com.error.log
```

---

## 🔒 GÜVENLİK KONTROLÜ

✅ `DEBUG=False` olmalı  
✅ `SECRET_KEY` unique olmalı (auto-generated)  
✅ `ALLOWED_HOSTS` doğru domain içermeli  
✅ Database şifresi güçlü olmalı  

---

## 📊 SONRAKI ADIMLAR

1. **Google OAuth** API keys ekleyin (eğer kullanıyorsanız)
2. **Email SMTP** ayarlarını yapın (gerçek email göndermek için)
3. **Fixture data** yükleyin:
   ```bash
   python manage.py loaddata fixtures/categories.json
   ```
4. **Scheduled tasks** ayarlayın (Tasks tab'ında)

---

## 🎊 BAŞARILI! COLLECTORIUM CANLIDA!

Artık siteniz:

✅ **Canlı:** https://erennezih.pythonanywhere.com  
✅ **Admin:** https://erennezih.pythonanywhere.com/admin  
✅ **HTTPS:** Otomatik  
✅ **Database:** MySQL çalışıyor  
✅ **Static:** WhiteNoise ile serve ediliyor  

---

## 📞 DESTEK

Sorun yaşarsanız:
- PythonAnywhere Forums
- Error logs kontrol
- Console'da debug

**Deployment başarılı olduğunda bana haber verin!** 🎉

