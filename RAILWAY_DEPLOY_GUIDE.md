# 🚂 COLLECTORIUM - RAILWAY DEPLOYMENT GUIDE

**Tam optimize edilmiş Railway deployment rehberi**

---

## ✅ HAZIRLIK DURUMU

Projeniz Railway için **tamamen optimize edilmiştir**:

- ✅ `Procfile` - Web + Release commands
- ✅ `runtime.txt` - Python 3.11
- ✅ `nixpacks.toml` - Build configuration
- ✅ `railway.json` - Deploy settings
- ✅ `.railwayignore` - Unnecessary files excluded
- ✅ `requirements.txt` - Production dependencies
- ✅ `collectorium/settings/railway.py` - Production settings
- ✅ `collectorium/wsgi.py` - WSGI optimized

---

## 🚀 DEPLOYMENT ADIMLARI

### 1. GitHub'a Push Edin

```bash
git add .
git commit -m "Railway deployment optimization complete"
git push
```

### 2. Railway'de Variables Ayarlayın

**Settings → Variables** tab'ında:

```
DJANGO_SETTINGS_MODULE = collectorium.settings.railway
SECRET_KEY = [Generate with: python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"]
DEBUG = False
```

**Opsiyonel (Google OAuth için):**
```
GOOGLE_CLIENT_ID = your-client-id
GOOGLE_CLIENT_SECRET = your-secret
```

### 3. Otomatik Deploy Başlayacak!

Railway GitHub commit'i algılayınca otomatik deploy başlar.

**Deploy Süreci:**
1. ✅ Python 3.11 kurulumu
2. ✅ PostgreSQL bağlantısı
3. ✅ Dependencies yükleme
4. ✅ Static files toplama (`collectstatic`)
5. ✅ Database migration
6. ✅ Gunicorn start (4 workers)

---

## 📊 DEPLOY SONRASI

### Site URL'nizi Alın

**Settings → Domains** → Railway size URL verecek:
```
https://collectorium-production.up.railway.app
```

### Superuser Oluşturun

**Deployments → Latest → ⋮ → Run a command:**
```bash
python manage.py createsuperuser
```

### Test Edin

```
https://your-app.up.railway.app/
https://your-app.up.railway.app/admin
https://your-app.up.railway.app/healthz/
```

---

## 🔧 OPTİMİZASYONLAR

Projenizde yapılan optimizasyonlar:

### Performance
- ✅ **4 Gunicorn workers** (concurrent requests)
- ✅ **Template caching** enabled
- ✅ **Database connection pooling** (600s)
- ✅ **WhiteNoise static compression**
- ✅ **Session database backend**

### Security
- ✅ **DEBUG=False** enforced
- ✅ **HTTPS redirect** enabled
- ✅ **Secure cookies** configured
- ✅ **CSRF protection** with Railway domains
- ✅ **Security headers** activated

### Deployment
- ✅ **Automatic migrations** on deploy
- ✅ **Automatic static collection**
- ✅ **Health check endpoint** (/healthz/)
- ✅ **Graceful restarts** on failure

---

## 🎯 GÜNCELLEMELER

Her kod değişikliğinde:

```bash
git add .
git commit -m "Your changes"
git push
```

Railway **otomatik olarak**:
1. Yeni commit'i algılar
2. Build yapar
3. Migrate çalıştırır
4. Collectstatic yapar
5. Deploy eder
6. Graceful restart yapar

**Zero downtime deployment!** 🚀

---

## 📈 MONİTORİNG

### Logs İzleme

**Deployments → Latest → View Logs**

### Health Check

```bash
curl https://your-app.up.railway.app/healthz/
```

Response:
```json
{"status": "healthy"}
```

---

## 🆘 TROUBLESHOOTING

### Deploy Failed

1. **Deployments → Logs** kontrol edin
2. **Variables** doğru mu kontrol edin
3. **SECRET_KEY** set edilmiş mi?

### Static Files Yüklenmiyor

- `collectstatic` otomatik çalışmalı (Procfile release command)
- WhiteNoise middleware aktif mi kontrol edin

### Database Error

- Railway DATABASE_URL otomatik set edilir
- PostgreSQL service eklenmiş mi kontrol edin

---

## 🎉 BAŞARILI!

Collectorium şimdi Railway'de production-ready durumda! 

**Özellikler:**
- ✅ Otomatik deployment
- ✅ PostgreSQL database
- ✅ Static files serving
- ✅ HTTPS enabled
- ✅ Auto-scaling ready
- ✅ Health monitoring

**Tadını çıkarın!** 🚀🎊

