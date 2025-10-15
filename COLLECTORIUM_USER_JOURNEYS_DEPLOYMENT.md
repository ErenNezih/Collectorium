# 🚀 COLLECTORIUM - KULLANICI YOLCULUKLARI VE DEPLOYMENT

**Bölüm:** 4/10 - Kullanıcı Akışları, Kurulum ve Canlıya Alma  
**Tarih:** 15 Ekim 2025

---

## 6. KULLANICI YOLCULUKLARI

### 6.1 Yeni Kullanıcı - Seller Kaydı (Google OAuth)

#### Adım 1: Ana Sayfa
```
Kullanıcı → https://collectorium.com
         → Hero bölümü ile karşılaşır (animasyonlu kartlar)
         → "Satıcı Ol" butonuna tıklar
```

#### Adım 2: Kayıt Sayfası
```
/accounts/signup/
├── Email/Username/Şifre formu VEYA
└── "Google ile Kayıt Ol" butonu ← TIKLAR
```

#### Adım 3: Google OAuth Flow
```
Google'a Yönlendirilme
├── Google hesabı seçimi
├── İzinleri onaylama
└── Callback → /accounts/google/login/callback/
```

#### Adım 4: Custom Adapter İnterception
```python
CustomSocialAccountAdapter.pre_social_login()
├── Kullanıcı yeni mi kontrol
├── Evet → Session'a Google verileri kaydet
└── Yönlendir → /accounts/google/signup/complete/
```

#### Adım 5: Onboarding Center
```
/accounts/google/signup/complete/
├── Form Alanları:
│   ├── Username (auto-suggest: googlefirstname123)
│   ├── Phone (05XX XXX XX XX)
│   ├── Phone Verification (simulated)
│   │   ├── "Kod Gönder" → Code input açılır
│   │   ├── Kod gir (herhangi 4+ karakter)
│   │   └── "Doğrula" → ✅ Onaylandı
│   ├── Address (Ev/İş, Şehir, İlçe, Adres, Posta Kodu)
│   └── Role → ☑ Alıcı  ☑ Satıcı ← SEÇİLİR
└── "Kaydı Tamamla" butonu
```

#### Adım 6: Backend İşlemler
```python
google_onboarding_complete() view:
├── User.objects.create_user()
│   ├── username (form)
│   ├── email (session - Google)
│   ├── first_name (session - Google)
│   ├── last_name (session - Google)
│   ├── role = 'seller'
│   └── phone (form)
├── Address.objects.create()
│   └── user, city, district, full_address, is_default=True
├── SocialAccount.objects.create()
│   ├── user
│   ├── provider='google'
│   └── uid (session)
├── if role=='seller':
│   └── Store.objects.create() ← OTOMATIK MAĞAZA!
│       ├── owner=user
│       ├── name="{username}'s Store"
│       └── slug="{username}-store"
├── Session temizleme
└── login(request, user)
```

#### Adım 7: Ana Sayfaya Yönlendirme
```
messages.success: "Hoş geldiniz, [İsim]! 🎉 Hesabınız başarıyla oluşturuldu."
→ Ana sayfa (authenticated)
→ Header'da "Profil" linki görünür
→ Seller ise "İlan Ver" butonu aktif
```

**Toplam Süre:** ~2 dakika  
**Adım Sayısı:** 7 (Google ile) vs ~15 (manuel kayıt)

---

### 6.2 Satıcı - İlan Oluşturma Akışı

#### Adım 1: Dashboard'a Giriş
```
Header → "İlan Ver" butonu
→ /listings/create/
```

**Güvenlik Kontrolleri:**
```python
@method_decorator(login_required)
@method_decorator(seller_required)
def dispatch(self, request, *args, **kwargs):
    # Sadece seller'lar erişebilir
```

#### Adım 2: İlan Formu
```
Listing Form:
├── Product: [Dropdown - Ürün kataloğundan seç]
│   └── Örn: "Blue-Eyes White Dragon - Konami"
├── Title: [Text] "Blue-Eyes White Dragon 1st Edition NM"
├── Description: [Textarea]
│   └── "Koleksiyonumdan çıkıyor. Mint durumda..."
├── Price: [Number] 1500.00 TRY
├── Condition: [Select]
│   └── ☑ Yeni / Sıfıra Yakın / İyi / Orta / Kötü
├── Stock: [Number] 1
└── Images: [Multiple File Upload]
    ├── Upload 1 (Primary)
    ├── Upload 2
    └── Upload 3
```

#### Adım 3: Backend İşlem
```python
ListingCreateView.form_valid():
├── form.instance.store = request.user.store  # Otomatik mağaza ataması
├── listing.save()
├── for image in request.FILES.getlist('images'):
│   └── ListingImage.objects.create(listing=listing, image=image)
└── messages.success("İlanınız başarıyla oluşturuldu.")
```

#### Adım 4: İlanlarım Sayfası
```
/account/my-listings/
├── Listing 1 [Düzenle] [Sil]
├── Listing 2 [Düzenle] [Sil]
└── [+ Yeni İlan Oluştur]
```

**Toplam Süre:** ~3-5 dakika  
**Adım Sayısı:** 4

---

### 6.3 Alıcı - Satın Alma Akışı

#### Adım 1: Ürün Arama
```
Marketplace → /marketplace/
├── Filters:
│   ├── Kategori: TCG
│   ├── Durum: Yeni
│   ├── Fiyat: 0-2000 TL
│   └── Sıralama: En Ucuz
└── 48 sonuç bulundu
```

**Backend Query:**
```python
listings = Listing.objects.filter(is_active=True)
    .filter(product__category__slug='tcg')
    .filter(condition='new')
    .filter(price__gte=0, price__lte=2000)
    .order_by('price')
```

#### Adım 2: İlan Detay
```
/listing/42/
├── Görsel Galeri (Alpine.js)
│   ├── Ana Görsel (büyük)
│   └── Thumbnails (4 adet, tıklanabilir)
├── Bilgiler:
│   ├── Başlık
│   ├── Fiyat: 1,500.00 TL
│   ├── Stok: 1 adet
│   ├── Durum: Yeni
│   ├── Kategori: TCG → Pokemon
│   └── Marka: Konami
├── Satıcı Kartı:
│   ├── Mağaza: "[Username]'s Store"
│   ├── Doğrulanmış rozeti ✓
│   └── [Mağazayı Ziyaret Et]
└── [Sepete Ekle] butonu
```

#### Adım 3: Sepete Ekleme
```
POST /cart/add/42/
├── CartAddListingForm:
│   ├── quantity: 1
│   └── override: False
├── Cart.add(listing, quantity)
├── session['cart']['42'] = {'quantity': 1, 'price': '1500.00'}
└── messages.success("Blue-Eyes White Dragon sepete eklendi.")
```

#### Adım 4: Sepet Görüntüleme
```
/cart/
├── Items:
│   ├── Blue-Eyes White Dragon
│   │   ├── Miktar: [1] [Güncelle] [Sil]
│   │   └── Fiyat: 1,500.00 TL
│   └── Pikachu Promo Card
│       ├── Miktar: [2] [Güncelle] [Sil]
│       └── Fiyat: 600.00 TL x 2 = 1,200.00 TL
├── Toplam: 2,700.00 TL
└── [Alışverişi Tamamla] → /orders/checkout/
```

#### Adım 5: Checkout (Adres Formu)
```
/orders/checkout/
├── Adres Seçimi:
│   └── ☑ Varsayılan Adres (Ev - İstanbul)
│   └── + Yeni Adres Ekle
├── Sepet Özeti:
│   ├── 2 ürün
│   └── Toplam: 2,700.00 TL
├── Notlar: [Textarea] (opsiyonel)
└── [Siparişi Onayla] butonu
```

#### Adım 6: Backend Sipariş Oluşturma
```python
order_create() view:
├── Order.objects.create(
│   buyer=request.user,
│   total=cart.get_total_price(),  # 2700.00
│   shipping_address=address.full_text,
│   status='pending'
│   )
├── for item in cart:
│   └── OrderItem.objects.create(
│       order=order,
│       listing=item['listing'],
│       quantity=item['quantity'],
│       price_snapshot=item['price']  # Fiyat değişse bile korunur
│       )
├── cart.clear()
└── messages.success("Siparişiniz oluşturuldu! Sipariş #42")
```

#### Adım 7: Sipariş Onay Sayfası
```
/orders/created/
├── Sipariş #42
├── Durum: Beklemede
├── Toplam: 2,700.00 TL
├── Ürünler:
│   ├── Blue-Eyes White Dragon x1
│   └── Pikachu Promo Card x2
└── Teslimat Adresi: [Ev - İstanbul]
```

**Toplam Süre:** ~5-8 dakika  
**Adım Sayısı:** 7

---

### 6.4 Admin - Mağaza Onaylama

#### Adım 1: Admin Panele Giriş
```
/admin/
├── Username: admin
└── Password: ****
```

#### Adım 2: Stores Yönetimi
```
Admin → Stores → Store objects
├── List:
│   ├── [✗] "NewSeller123's Store" (is_verified=False)
│   ├── [✓] "TrustySeller's Store" (is_verified=True)
│   └── [✗] "AnotherStore" (is_verified=False)
```

#### Adım 3: Mağaza Düzenleme
```
Store: "NewSeller123's Store"
├── Owner: newuser@gmail.com
├── Name: NewSeller123's Store
├── Slug: newseller123-store
├── Bio: "Yeni mağazam..."
├── Logo: [No file]
├── ☑ is_verified ← İŞARETLE
└── [Save]
```

#### Adım 4: Sonuç
```
→ Mağaza artık marketplace'de görünür
→ /stores/ listesinde yer alır
→ Kullanıcı bildirim alır (opsiyonel - gelecekte)
```

---

## 9. KURULUM VE DEPLOYMENT

### 9.1 Lokal Geliştirme Ortamı Kurulumu

#### Gereksinimler
- Python 3.10+
- pip
- Git
- (Opsiyonel) virtualenv

#### Adım Adım Kurulum

**1. Repository Clone**
```bash
git clone https://github.com/yourusername/collectorium.git
cd collectorium
```

**2. Virtual Environment**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

**3. Bağımlılıkları Yükle**
```bash
pip install -r requirements.txt
```

**4. Environment Variables**
```bash
# .env dosyası oluştur (env.example'dan kopyala)
cp env.example .env

# .env dosyasını düzenle:
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=127.0.0.1,localhost
DATABASE_URL=  # Boş bırakabilirsiniz (SQLite kullanacak)
GOOGLE_CLIENT_ID=  # Google OAuth için (opsiyonel)
GOOGLE_CLIENT_SECRET=  # Google OAuth için (opsiyonel)
```

**5. Veritabanı Migration**
```bash
python manage.py migrate
```

**6. Örnek Veri Yükle (Opsiyonel)**
```bash
python manage.py loaddata fixtures/sample_data.json
```

**7. Superuser Oluştur**
```bash
python manage.py createsuperuser
# Username: admin
# Email: admin@collectorium.com
# Password: [güçlü bir şifre]
```

**8. Google OAuth Kurulumu (Opsiyonel)**
```bash
python manage.py setup_google_oauth
# Talimatları takip edin
```

**9. Sunucuyu Başlat**
```bash
python manage.py runserver
```

**10. Tarayıcıda Aç**
```
http://127.0.0.1:8000/
```

---

### 9.2 Production Deployment (Heroku)

#### Ön Gereksinimler
- Heroku hesabı
- Heroku CLI kurulu
- Git

#### Adım Adım Deployment

**1. Heroku Giriş**
```bash
heroku login
```

**2. Heroku App Oluştur**
```bash
heroku create collectorium-app
```

**3. PostgreSQL Addon Ekle**
```bash
heroku addons:create heroku-postgresql:mini
```

**4. Environment Variables Ayarla**
```bash
heroku config:set DEBUG=False
heroku config:set SECRET_KEY=$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')
heroku config:set ALLOWED_HOSTS=collectorium-app.herokuapp.com
heroku config:set GOOGLE_CLIENT_ID=your-google-client-id
heroku config:set GOOGLE_CLIENT_SECRET=your-google-secret
```

**5. Deploy**
```bash
git push heroku main
```

**6. Migration Çalıştır**
```bash
heroku run python manage.py migrate
```

**7. Superuser Oluştur**
```bash
heroku run python manage.py createsuperuser
```

**8. Örnek Veri Yükle (Opsiyonel)**
```bash
heroku run python manage.py loaddata fixtures/sample_data.json
```

**9. Google OAuth Kurulumu**
```bash
heroku run python manage.py setup_google_oauth
```

**10. App'i Aç**
```bash
heroku open
```

#### Önemli Notlar

**Procfile (zaten mevcut):**
```
web: gunicorn collectorium.wsgi --log-file -
```

**Static Files:**
- WhiteNoise otomatik olarak statik dosyaları serve ediyor
- `python manage.py collectstatic` gerekli değil (otomatik)

**Media Files:**
- Production'da media dosyaları için AWS S3 veya Cloudinary önerilir
- Heroku ephemeral filesystem (dosyalar kaybolabilir)

**Database:**
- Heroku PostgreSQL otomatik olarak `DATABASE_URL` env variable'ı sağlıyor
- `dj-database-url` paketi ile otomatik parse ediliyor

---

### 9.3 Production Checklist

#### Güvenlik
- [ ] `DEBUG = False`
- [ ] Güçlü `SECRET_KEY` (environment variable)
- [ ] `ALLOWED_HOSTS` doğru ayarlandı
- [ ] HTTPS zorunlu (`SECURE_SSL_REDIRECT = True`)
- [ ] CSRF koruması aktif (varsayılan)
- [ ] XSS koruması aktif (varsayılan)
- [ ] SQL Injection koruması (Django ORM kullanımı)

#### Performance
- [ ] `DEBUG_TOOLBAR` devre dışı (production'da otomatik)
- [ ] Statik dosyalar WhiteNoise ile serve ediliyor
- [ ] Database indeksleri oluşturuldu
- [ ] Query optimizasyonu (`select_related`, `prefetch_related`)
- [ ] Pagination tüm list view'larda
- [ ] Görsel optimizasyonu (Pillow ile resize)

#### Monitoring
- [ ] Heroku logs aktif (`heroku logs --tail`)
- [ ] Error tracking (Sentry öneriliyor)
- [ ] Uptime monitoring (UptimeRobot, Pingdom)
- [ ] Performance monitoring (New Relic, Scout APM)

#### Backup
- [ ] PostgreSQL otomatik backup aktif (Heroku)
- [ ] Media dosyaları S3'e yedekleniyor
- [ ] Günlük veritabanı export (opsiyonel)

#### SEO
- [ ] Sitemap oluşturuldu (`django.contrib.sitemaps`)
- [ ] robots.txt yapılandırıldı
- [ ] Meta tags tüm sayfalarda
- [ ] Open Graph tags (sosyal medya paylaşımı için)
- [ ] Analytics entegrasyonu (Google Analytics)

---

### 9.4 Maintenance ve Updates

#### Günlük Görevler
- Log kontrolü (`heroku logs --tail`)
- Yeni sipariş kontrolü (admin panel)
- Kullanıcı geri bildirimleri

#### Haftalık Görevler
- Database backup kontrolü
- Disk kullanımı kontrolü
- Security update'leri

#### Aylık Görevler
- Django ve paket güncellemeleri
- Performance analizi
- Kullanıcı istatistikleri raporu

---

### 9.5 Sorun Giderme

#### "Application Error" Hatası
```bash
# Logları kontrol et
heroku logs --tail

# Database migration gerekebilir
heroku run python manage.py migrate

# Config vars kontrol et
heroku config
```

#### Statik Dosyalar Yüklenmiyor
```bash
# Collectstatic çalıştır
heroku run python manage.py collectstatic --noinput

# WhiteNoise ayarlarını kontrol et
# settings.py → MIDDLEWARE'de WhiteNoiseMiddleware olmalı
```

#### Google OAuth Çalışmıyor
```bash
# 1. Google Cloud Console'da redirect URI kontrol et
#    https://your-app.herokuapp.com/accounts/google/login/callback/

# 2. Admin panelde Social Application ayarlarını kontrol et

# 3. Site domain'ini güncelle
heroku run python manage.py shell
>>> from django.contrib.sites.models import Site
>>> site = Site.objects.get(id=1)
>>> site.domain = 'your-app.herokuapp.com'
>>> site.name = 'Collectorium'
>>> site.save()
```

#### 500 Internal Server Error
```bash
# Detaylı hata için DEBUG=True yap (geçici)
heroku config:set DEBUG=True

# Hatayı gör
heroku logs --tail

# Düzelttikten sonra DEBUG=False yap
heroku config:set DEBUG=False
```

---

## 10. API VE ENTEGRASYONLAR

### 10.1 Mevcut Entegrasyonlar

#### django-allauth (Google OAuth)
- **Durum:** ✅ Aktif ve Çalışıyor
- **Amaç:** Kullanıcı kimlik doğrulama
- **Özellikler:**
  - Google ile giriş/kayıt
  - Özel onboarding akışı
  - Hesap bağlama/bağlantı kaldırma

#### HTMX
- **Durum:** ✅ Entegre
- **Amaç:** Asenkron sayfa güncellemeleri
- **Kullanım Alanları:**
  - Sepete ekleme (sayfa yenilenmeden)
  - Form submit (partial update)
  - Dinamik içerik yükleme

#### Alpine.js
- **Durum:** ✅ Entegre
- **Amaç:** Hafif client-side interaktivite
- **Kullanım Alanları:**
  - Görsel galerisi (listing detail)
  - Telefon onayı simülasyonu (onboarding)
  - Dropdown menüler
  - Flash message otomatik kapanma

### 10.2 Gelecek Entegrasyonlar

#### Ödeme Gateway'leri
- **İyzico** (Türkiye için popüler)
- **Stripe** (global)
- **PayPal**

#### Kargo Firmaları
- **Aras Kargo** API
- **MNG Kargo** API
- **Yurtiçi Kargo** API

#### Mesajlaşma
- **WebSocket** (Django Channels)
- **Real-time chat** (satıcı-alıcı)

#### Bildirimler
- **Email:** `django-mailer`
- **Push Notifications:** Firebase Cloud Messaging
- **SMS:** Twilio veya NetGsm

---

**Dokümantasyon devam ediyor... (Sayfa 4/10)**

*Sonraki bölümde: Gelecek geliştirmeler, API dokümantasyonu ve katkıda bulunma rehberi.*
