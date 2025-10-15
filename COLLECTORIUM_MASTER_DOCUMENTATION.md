# 📚 COLLECTORIUM - KAPSAMLI MASTER DOKÜMANTASYON

**Proje:** Collectorium - Türkiye'nin İlk Niş Koleksiyon Pazar Yeri  
**Versiyon:** Beta 1.0  
**Tarih:** 15 Ekim 2025  
**Durum:** ✅ Tam Fonksiyonel, Canlıya Hazır

---

## 📖 İÇİNDEKİLER

1. [Proje Genel Bakış](#1-proje-genel-bakış)
2. [Teknoloji Yığını](#2-teknoloji-yığını)
3. [Sistem Mimarisi](#3-sistem-mimarisi)
4. [Django Uygulamaları Detaylı Analiz](#4-django-uygulamaları-detaylı-analiz)
5. [Veritabanı Yapısı](#5-veritabanı-yapısı)
6. [Kullanıcı Yolculukları](#6-kullanıcı-yolculukları)
7. [Özellik Detayları](#7-özellik-detayları)
8. [Operasyon Geçmişi](#8-operasyon-geçmişi)
9. [Kurulum ve Deployment](#9-kurulum-ve-deployment)
10. [API ve Entegrasyonlar](#10-api-ve-entegrasyonlar)
11. [Güvenlik ve Best Practices](#11-güvenlik-ve-best-practices)
12. [Gelecek Geliştirmeler](#12-gelecek-geliştirmeler)

---

## 1. PROJE GENEL BAKIŞ

### 1.1 Misyon ve Vizyon

**Misyon:**  
Türkiye'de koleksiyon tutkunlarının güvenli, profesyonel ve kullanıcı dostu bir platformda TCG kartları, figürler, comicler ve diğer koleksiyon ürünlerini alıp satabilecekleri niş bir pazar yeri oluşturmak.

**Vizyon:**  
Koleksiyon dünyasının en güvenilir ve kapsamlı çevrimiçi ticaret merkezi olmak.

### 1.2 Temel Özellikler

#### Alıcılar İçin (Buyers):
- ✅ Gelişmiş arama ve filtreleme (kategori, fiyat, durum, satıcı)
- ✅ Detaylı ürün görüntüleme (çoklu resim, zoom, ürün özellikleri)
- ✅ Session-based alışveriş sepeti
- ✅ Adres yönetimi ve sipariş takibi
- ✅ Favori ilanlar (favorilere ekleme)
- ✅ Değerlendirme ve yorum sistemi

#### Satıcılar İçin (Sellers):
- ✅ Otomatik mağaza oluşturma (kayıt anında)
- ✅ İlan CRUD operasyonları (Create, Read, Update, Delete)
- ✅ Çoklu resim yükleme
- ✅ Stok yönetimi
- ✅ Sipariş yönetimi
- ✅ Satıcı paneli (dashboard)

#### Platform Özellikleri:
- ✅ Modern, responsive tasarım (TailwindCSS)
- ✅ Google OAuth 2.0 ile akıllı onboarding
- ✅ Flash mesajları (kullanıcı geri bildirimi)
- ✅ Özel hata sayfaları (404, 500, 403)
- ✅ SEO dostu URL yapısı
- ✅ Admin paneli (Django Admin - özelleştirilmiş)

### 1.3 Proje İstatistikleri

| Metrik | Değer |
|--------|-------|
| **Toplam Django Uygulaması** | 13 adet |
| **Toplam Model** | 15+ adet |
| **Toplam View** | 40+ adet |
| **Toplam Template** | 50+ adet |
| **Toplam URL Pattern** | 60+ adet |
| **Kod Satırı** | ~8,000+ satır (Python + HTML + CSS) |
| **Bağımlılık Paketi** | 20+ paket |
| **Operasyon Sayısı** | 5 büyük operasyon |

---

## 2. TEKNOLOJİ YIĞINI

### 2.1 Backend Stack

| Teknoloji | Versiyon | Kullanım Amacı |
|-----------|----------|----------------|
| **Python** | 3.10+ | Ana programlama dili |
| **Django** | 5.2.* | Web framework |
| **SQLite** | 3 | Geliştirme veritabanı |
| **PostgreSQL** | - | Production veritabanı (opsiyonel) |
| **django-allauth** | 65.* | Kimlik doğrulama ve OAuth |
| **Pillow** | 11.* | Görsel işleme |
| **WhiteNoise** | 6.* | Statik dosya servisi |
| **dj-database-url** | 3.* | Veritabanı URL parsing |

### 2.2 Frontend Stack

| Teknoloji | Kullanım Amacı |
|-----------|----------------|
| **TailwindCSS** | Utility-first CSS framework |
| **Alpine.js** | Hafif JavaScript framework (interaktivite) |
| **HTMX** | HTML-over-the-wire framework |
| **Google Fonts** | Orbitron (başlık), Poppins (metin) |

### 2.3 Development Tools

| Tool | Kullanım Amacı |
|------|----------------|
| **Black** | Python kod formatlama |
| **isort** | Import sıralama |
| **Flake8** | Linting |
| **pytest** | Test framework |
| **django-debug-toolbar** | Geliştirme debugging |

### 2.4 Deployment Stack

| Platform | Kullanım Amacı |
|----------|----------------|
| **Heroku** | Cloud hosting (Procfile mevcut) |
| **Gunicorn** | WSGI HTTP Server |
| **WhiteNoise** | Statik dosya servisi |

---

## 3. SİSTEM MİMARİSİ

### 3.1 Proje Yapısı

```
collectorium/
├── collectorium/              # Proje ayarları (settings, URLs)
│   ├── __init__.py
│   ├── settings.py           # ⭐ Ana yapılandırma
│   ├── urls.py               # ⭐ Root URL dispatcher
│   ├── wsgi.py
│   └── asgi.py
│
├── accounts/                  # Kullanıcı yönetimi
│   ├── models.py             # User, Address
│   ├── views.py              # Profil, şifre değiştir, onboarding
│   ├── adapters.py           # ⭐ Google OAuth özel adapter
│   ├── forms.py              # GoogleOnboardingForm
│   ├── admin.py              # Özelleştirilmiş admin
│   ├── signals.py            # Otomatik mağaza oluşturma
│   ├── mixins.py             # SellerRequiredMixin
│   └── management/
│       └── commands/
│           └── setup_google_oauth.py  # ⭐ Kurulum komutu
│
├── stores/                    # Mağaza yönetimi
│   ├── models.py             # Store
│   ├── views.py              # Mağaza listesi, detay
│   └── admin.py
│
├── listings/                  # İlan yönetimi
│   ├── models.py             # Listing, ListingImage, Favorite
│   ├── views.py              # CRUD operasyonları
│   ├── forms.py              # ListingForm, ImageUploadForm
│   ├── mixins.py             # ListingOwnerRequiredMixin
│   └── admin.py
│
├── catalog/                   # Ürün kataloğu
│   ├── models.py             # Category, Product
│   ├── views.py              # Kategori listesi
│   └── admin.py
│
├── cart/                      # Alışveriş sepeti
│   ├── cart.py               # ⭐ Session-based Cart sınıfı
│   ├── views.py              # Sepete ekle/çıkar/göster
│   ├── forms.py              # CartAddListingForm
│   └── context_processors.py # Global cart objesi
│
├── orders/                    # Sipariş yönetimi
│   ├── models.py             # Order, OrderItem
│   ├── views.py              # Checkout, order_created
│   ├── forms.py              # OrderCreateForm
│   └── admin.py
│
├── reviews/                   # Değerlendirme sistemi
│   ├── models.py             # Review
│   └── admin.py
│
├── core/                      # Ana uygulama
│   ├── views.py              # Home, marketplace, statik sayfalar
│   └── urls.py               # Ana URL'ler
│
├── messaging/                 # Mesajlaşma (gelecek)
├── moderation/                # İçerik moderasyonu (gelecek)
├── payments/                  # Ödeme sistemleri (gelecek)
├── search/                    # Gelişmiş arama (gelecek)
├── shipping/                  # Kargo entegrasyonu (gelecek)
├── dashboards/                # Dashboard (gelecek)
│
├── templates/                 # ⭐ Merkezi template klasörü
│   ├── base.html             # Ana şablon (header, footer, CSS)
│   ├── home.html             # Ana sayfa (hero bölümü)
│   ├── marketplace.html      # İlan listesi
│   ├── listing_detail.html   # İlan detay
│   ├── includes/
│   │   ├── header.html
│   │   └── footer.html
│   ├── account/              # Allauth şablonları
│   ├── accounts/             # Kullanıcı şablonları
│   ├── socialaccount/        # ⭐ Google OAuth şablonları
│   ├── listings/
│   ├── cart/
│   ├── orders/
│   ├── stores/
│   ├── pages/                # Statik sayfalar
│   └── 404.html, 500.html, 403.html
│
├── static/                    # Statik dosyalar
│   ├── css/
│   │   └── custom.css
│   └── images/
│       └── hero/             # ⭐ Hero bölümü görselleri
│           ├── hero_background.jpg
│           ├── hero_item_1.png ~ hero_item_6.png
│
├── media/                     # Kullanıcı yüklü dosyalar
│   ├── avatars/
│   ├── listing_images/
│   └── store_logos/
│
├── fixtures/                  # Örnek veri
│   ├── sample_data.json
│   └── seed.json
│
├── venv/                      # Virtual environment
├── db.sqlite3                 # SQLite veritabanı
├── manage.py                  # Django management script
├── requirements.txt           # Python bağımlılıkları
├── Procfile                   # Heroku deployment
├── pyproject.toml             # Proje metadata
├── README.md                  # Temel README
├── GOOGLE_OAUTH_SETUP.md      # ⭐ Google OAuth kurulum rehberi
├── AEGIS_OPERATION_REPORT.md  # ⭐ Operasyon raporu
└── COLLECTORIUM_MASTER_DOCUMENTATION.md  # ⭐ Bu dosya
```

### 3.2 URL Yapısı

| URL Pattern | View | Açıklama |
|-------------|------|----------|
| `/` | `core.views.home` | Ana sayfa |
| `/marketplace/` | `core.views.marketplace` | İlan listesi + filtreler |
| `/listing/<id>/` | `core.views.listing_detail` | İlan detay |
| `/listings/create/` | `listings.views.ListingCreateView` | Yeni ilan (seller only) |
| `/listings/<pk>/edit/` | `listings.views.ListingUpdateView` | İlan düzenle |
| `/listings/<pk>/delete/` | `listings.views.ListingDeleteView` | İlan sil |
| `/cart/` | `cart.views.cart_detail` | Sepet |
| `/cart/add/<id>/` | `cart.views.cart_add` | Sepete ekle |
| `/orders/checkout/` | `orders.views.order_create` | Ödeme sayfası |
| `/stores/` | `stores.views.stores_list` | Mağaza listesi |
| `/stores/<slug>/` | `stores.views.store_detail` | Mağaza detay |
| `/categories/` | `catalog.views.categories_list` | Kategori listesi |
| `/account/profile/` | `accounts.views.profile` | Kullanıcı profili |
| `/account/orders/` | `accounts.views.my_orders` | Siparişlerim |
| `/account/my-listings/` | `accounts.views.MyListingsView` | İlanlarım |
| `/accounts/login/` | `allauth` | Giriş yap |
| `/accounts/signup/` | `allauth` | Kayıt ol |
| `/accounts/google/login/callback/` | `allauth` | Google OAuth callback |
| `/accounts/google/signup/complete/` | `accounts.views.google_onboarding_complete` | ⭐ Özel onboarding |
| `/admin/` | Django Admin | Yönetim paneli |

### 3.3 Veri Akışı Mimarisi

```
┌─────────────┐
│   Browser   │
└──────┬──────┘
       │
       ▼
┌─────────────────────────┐
│   Django Middleware     │
│   - Security            │
│   - Session             │
│   - CSRF                │
│   - Authentication      │
│   - Messages            │
└──────┬──────────────────┘
       │
       ▼
┌─────────────────────────┐
│   URL Dispatcher        │
│   (collectorium/urls)   │
└──────┬──────────────────┘
       │
       ▼
┌─────────────────────────┐
│   View Layer            │
│   - FBV / CBV           │
│   - Business Logic      │
│   - Form Validation     │
└──────┬──────────────────┘
       │
       ▼
┌─────────────────────────┐
│   Model Layer (ORM)     │
│   - Database Queries    │
│   - Data Validation     │
└──────┬──────────────────┘
       │
       ▼
┌─────────────────────────┐
│   SQLite / PostgreSQL   │
└─────────────────────────┘
       │
       ▼
┌─────────────────────────┐
│   Template Engine       │
│   - Django Templates    │
│   - Context Rendering   │
└──────┬──────────────────┘
       │
       ▼
┌─────────────────────────┐
│   Browser (HTML/CSS/JS) │
│   - TailwindCSS         │
│   - Alpine.js           │
│   - HTMX                │
└─────────────────────────┘
```

---

**Dokümantasyon devam ediyor... (Sayfa 1/10)**

---

*Not: Bu dokümantasyon çok kapsamlı olduğu için bölümler halinde sunulmuştur. Diğer bölümler için lütfen `COLLECTORIUM_TECHNICAL_DEEP_DIVE.md` dosyasına bakınız.*
