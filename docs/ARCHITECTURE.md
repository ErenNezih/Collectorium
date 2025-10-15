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


