# 🏗️ Collectorium Architecture

Bu doküman, uygulamanın mimarisini, ana modülleri ve veri akışını özetler.

## Uygulama Modülleri

- accounts: Kimlik, profil, adres, Google OAuth
- stores: Mağaza modeli ve sayfaları
- listings: İlan modeli, görseller, CRUD
- catalog: Kategori ve ürün
- cart: Session tabanlı sepet
- orders: Sipariş ve sipariş kalemi
- reviews: İlan yorumları
- core: Ana sayfa, marketplace, health endpoints

## URL Haritası (özet)

- / → core.views.home
- /marketplace/ → core.views.marketplace
- /listing/<id>/ → core.views.listing_detail
- /accounts/ → allauth + accounts.urls
- /cart/, /orders/, /stores/, /categories/
- /healthz, /health/readiness, /health/liveness

## Veri Modeli (seçmeler)

- accounts.User(role, avatar, phone, ...)
- accounts.Address(user, full_address, is_default)
- stores.Store(owner, slug, is_verified)
- catalog.Category(parent self-FK), Product(category, name, brand)
- listings.Listing(store, product, price, condition, is_active)
- listings.ListingImage(listing, image, is_primary)
- reviews.Review(user, listing, rating, comment)
- orders.Order(buyer, total, status, shipping_address)
- orders.OrderItem(order, listing, quantity, price_snapshot)

## Google OAuth Akışı

1. Kullanıcı allauth ile Google’a gider
2. `CustomSocialAccountAdapter.pre_social_login` yeni kullanıcıyı tespit eder
3. Google verileri session’a yazılır ve onboarding’e yönlendirilir
4. `google_onboarding_complete` → User + Address + SocialAccount (+Store) oluşturur

## Performans Notları

- Query optimizasyonu: select_related/prefetch_related
- Statikler: WhiteNoise ile servis
- Template caching: Render için aktif (APP_DIRS=False + cached loader)

## Güvenlik

- Prod: HSTS, SSL redirect, secure cookies
- CSRF trusted origins ve ALLOWED_HOSTS zorunlu

# 🏗️ COLLECTORIUM - MİMARİ DOKÜMANTASYONU

## Proje Yapısı

Collectorium, modern Django best practices'e uygun olarak organize edilmiş bir monorepo yapısındadır.

### Dizin Organizasyonu

```
collectorium/
├── backend/                    # Django backend (ana kod tabanı)
│   ├── accounts/              # Kullanıcı yönetimi
│   ├── stores/                # Mağaza yönetimi
│   ├── listings/              # İlan sistemi
│   ├── catalog/               # Ürün kataloğu
│   ├── cart/                  # Sepet
│   ├── orders/                # Sipariş yönetimi
│   ├── reviews/               # Değerlendirmeler
│   ├── core/                  # Temel uygulama
│   ├── messaging/             # Mesajlaşma (future)
│   ├── moderation/            # Moderasyon (future)
│   ├── payments/              # Ödeme (future)
│   ├── search/                # Arama (future)
│   ├── shipping/              # Kargo (future)
│   └── dashboards/            # Dashboard (future)
│
├── frontend/                   # Static files & Tailwind
│   ├── static/                # Source static files
│   │   ├── css/              # Custom CSS
│   │   └── images/           # Images
│   ├── staticfiles/           # Collected static (generated)
│   └── package.json           # Node dependencies
│
├── infra/                      # Infrastructure & Deployment
│   ├── docker/                # Docker configurations
│   │   ├── Dockerfile
│   │   ├── docker-compose.yml
│   │   └── docker-compose.prod.yml
│   ├── deploy/                # Deployment scripts
│   │   ├── heroku/
│   │   └── railway/
│   └── scripts/               # Utility scripts
│
├── docs/                       # Documentation
│   ├── ARCHITECTURE.md        # This file
│   ├── API.md                 # API documentation
│   ├── DEPLOYMENT.md          # Deployment guide
│   └── RUNBOOK.md             # Operations runbook
│
├── tests/                      # Test suite
│   ├── unit/                  # Unit tests
│   ├── integration/           # Integration tests
│   ├── e2e/                   # End-to-end tests
│   └── load/                  # Load tests
│
├── collectorium/               # Django project settings
│   ├── settings/              # Split settings
│   │   ├── base.py
│   │   ├── dev.py
│   │   ├── stage.py
│   │   └── prod.py
│   ├── urls.py
│   └── wsgi.py
│
├── templates/                  # Django templates
├── media/                      # User uploads
├── fixtures/                   # Seed data
├── manage.py                   # Django management
├── pyproject.toml              # Python project config
├── .python-version             # Python version
├── .env.example                # Environment template
├── .gitignore                  # Git ignore
└── README.md                   # Main README
```

## Mevcut Yapı (Backward Compatible)

Mevcut proje yapısı korunmuştur. Yeni organizasyon mevcut yapının **üzerine** eklenmiştir:

- Django apps hala root seviyesinde (accounts, stores, vb.)
- `static/` ve `staticfiles/` mevcut konumlarında
- `templates/` root seviyesinde
- `collectorium/` project config klasörü mevcut

Bu yaklaşım:
- ✅ Mevcut kodu bozmaz
- ✅ Import path'leri değiştirmez
- ✅ Deployment pipeline'ı etkilemez
- ✅ Kademeli migration'a izin verir

## İleride Taşıma (Opsiyonel)

Gelecekte tüm Django apps'i `backend/` altına taşımak istenirse:

```bash
# Tüm apps'i backend/ altına taşı
mkdir -p backend
mv accounts stores listings catalog cart orders reviews core backend/

# settings.py'de app path'lerini güncelle
# INSTALLED_APPS = ['backend.accounts', 'backend.stores', ...]
```

**Not:** Şu an için bu taşıma **GEREKLİ DEĞİL**. Mevcut yapı production-ready'dir.


