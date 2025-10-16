# 🎯 Collectorium

Türkiye'nin ilk niş koleksiyon pazar yeri (Django 5.2, Render.com üzerinde canlı).

[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/)
[![Django 5.2](https://img.shields.io/badge/django-5.2-green.svg)](https://www.djangoproject.com/)
[![Render](https://img.shields.io/badge/host-Render.com-purple.svg)](https://render.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 📋 İçindekiler

- [Özellikler](#-özellikler)
- [Kurulum](#-kurulum)
- [Geliştirme](#-geliştirme)
- [Test](#-test)
- [Deployment](#-deployment)
- [Dokümantasyon](#-dokümantasyon)

---

## ✨ Özellikler

### 👥 Kullanıcı Sistemi
- **Alıcı & Satıcı Rolleri**: İki farklı kullanıcı tipi
- **Google OAuth**: Tek tıkla giriş
- **Akıllı Onboarding**: Yeni kullanıcılar için rehberli kayıt

### 🏪 Mağaza Yönetimi
- Satıcılar için özel mağaza sayfaları
- Mağaza doğrulama sistemi
- Satıcı profili ve biyografi

### 📦 İlan Sistemi
- CRUD operasyonları (Oluştur, Oku, Güncelle, Sil)
- Çoklu görsel desteği
- Stok takibi
- Durum yönetimi (yeni, ikinci el, vb.)

### 🛒 Sepet & Checkout
- Session-based sepet sistemi
- Adres yönetimi
- End-to-end sipariş akışı

### 🔍 Arama & Filtreleme
- Kategori bazlı arama
- Gelişmiş filtreleme seçenekleri
- Dinamik marketplace

---

## 🚀 Hızlı Başlangıç (Local)

Gereksinimler: Python 3.12.3, pip, (opsiyonel) PostgreSQL.

```bash
# 1. Depoyu klonlayın
git clone https://github.com/ErenNezih/Collectorium.git
cd collectorium

# 2. Virtual environment oluşturun
python -m venv venv
venv\Scripts\activate  # macOS/Linux: source venv/bin/activate

# 3. Bağımlılıkları yükleyin
pip install -r requirements.txt

# 4. Environment variables ayarlayın
copy env.example .env   # macOS/Linux: cp env.example .env

# 5. Database migration
python manage.py migrate

# 6. Fixture data yükleyin (opsiyonel)
python manage.py loaddata fixtures/categories.json

# 7. Superuser oluşturun
python manage.py createsuperuser

# 8. Development server'ı başlatın
python manage.py runserver
```

Tarayıcı:
- Uygulama: http://127.0.0.1:8000
- Sağlık: http://127.0.0.1:8000/healthz/

---

## 🛠️ Geliştirme

### Makefile Komutları

```bash
make install        # Tüm bağımlılıkları yükle
make run            # Development server başlat
make test           # Testleri çalıştır
make lint           # Linting kontrolleri
make format         # Kodu otomatik formatla
make migrate        # Database migration
make clean          # Geçici dosyaları temizle
```

### Django Settings

Proje 3 farklı ortam ayarına sahiptir:

- **Development** (`collectorium.settings.dev`): Lokal geliştirme
- **Staging** (`collectorium.settings.stage`): Pre-production test
- **Production** (`collectorium.settings.prod`): Canlı ortam

Ortam değiştirmek için:

```bash
export DJANGO_ENV=dev     # veya stage, prod
export DJANGO_SETTINGS_MODULE=collectorium.settings.dev
```

### Pre-commit Hooks

```bash
# Pre-commit hooks'u yükleyin
pre-commit install

# Manuel çalıştırma
pre-commit run --all-files
```

---

## 🧪 Test

### Unit Tests (Pytest)

```bash
# Tüm testleri çalıştır
pytest

# Coverage raporu ile
pytest --cov=. --cov-report=html

# Sadece unit testler
pytest -m unit

# Sadece integration testler
pytest -m integration
```

### E2E Tests (Playwright)

```bash
# Playwright browser'ları yükle (ilk kez)
playwright install

# E2E testleri çalıştır
pytest tests/e2e/ --headed  # Browser UI ile
pytest tests/e2e/           # Headless
```

### Load Tests (Locust)

```bash
# Locust'u başlat
locust -f tests/load/locustfile.py --host=http://127.0.0.1:8000

# Tarayıcıda http://localhost:8089 açın
```

### Health Checks

```bash
# Health endpoint
curl http://127.0.0.1:8000/healthz/

# Readiness probe
curl http://127.0.0.1:8000/health/readiness/

# Liveness probe
curl http://127.0.0.1:8000/health/liveness/
```

---

## 🌐 Dağıtım (Render)

Render üzerinde otomatik dağıtım etkindir. Temel kurallar:
- Build Command: `bash ./build.sh`
- Start Command: `bash ./start.sh`
- Gerekli env’ler: `DJANGO_SETTINGS_MODULE=collectorium.settings.render`, `DATABASE_URL` (Render Postgres), `ALLOWED_HOSTS=<servis>.onrender.com`, `SECRET_KEY`, `DEBUG=False`.

Ayrıntılar: `docs/DEPLOYMENT_RENDER.md`

---

## 📚 Belgeler

Detaylı dokümantasyon için:

- `docs/ARCHITECTURE.md` — Mimari ve akışlar
- `docs/DEVELOPMENT.md` — Lokal geliştirme, test ve kalite
- `docs/DEPLOYMENT_RENDER.md` — Render dağıtımı ve sorun giderme
- `RUNBOOK.md` — Operasyon rehberi (sağlık, log, rollback)
- `DEPLOY_LOG.md` — Son dağıtımların özeti

---

## 🏗️ Proje Yapısı

```
collectorium/
├── accounts/           # Kullanıcı yönetimi
├── stores/            # Mağaza sistemi
├── listings/          # İlan yönetimi
├── catalog/           # Ürün kataloğu
├── cart/              # Sepet
├── orders/            # Sipariş yönetimi
├── core/              # Temel uygulama
├── collectorium/      # Django project settings
│   └── settings/      # Ortam-bazlı ayarlar
├── templates/         # HTML şablonları
├── static/            # Static dosyalar
├── tests/             # Test suite
│   ├── unit/          # Unit tests
│   ├── integration/   # Integration tests
│   ├── e2e/           # End-to-end tests
│   └── load/          # Load tests
├── docs/              # Dokümantasyon
├── fixtures/          # Seed data
└── scripts/           # Utility scripts
```

---

## 🤝 Katkıda Bulunma

1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Değişikliklerinizi commit edin (`git commit -m 'Add amazing feature'`)
4. Branch'inizi push edin (`git push origin feature/amazing-feature`)
5. Pull Request açın

---

## 📝 Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için [LICENSE](LICENSE) dosyasına bakın.

---

## 👨‍💻 İletişim

info@collectorium.com

---

## 🙏 Teşekkürler

- Django Framework
- TailwindCSS
- Alpine.js
- htmx
- django-allauth
- Ve tüm açık kaynak topluluk!

---

Son Güncelleme: 2025-10-16
