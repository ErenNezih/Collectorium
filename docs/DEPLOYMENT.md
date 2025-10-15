# 🚀 COLLECTORIUM - DEPLOYMENT GUIDE

## Deployment Seçenekleri

Bu rehber, Collectorium'u farklı platformlara deploy etmek için adım adım talimatlar içerir.

---

## 📋 Pre-Deployment Checklist

Deployment öncesi mutlaka kontrol edin:

- [ ] `SECRET_KEY` production-ready (uzun, rastgele, güvenli)
- [ ] `DEBUG = False` production settings'de
- [ ] `ALLOWED_HOSTS` doğru şekilde ayarlanmış
- [ ] `CSRF_TRUSTED_ORIGINS` tanımlı
- [ ] PostgreSQL database yapılandırılmış
- [ ] Static files test edilmiş (`collectstatic`)
- [ ] Migration'lar hazır
- [ ] Environment variables tanımlı
- [ ] Google OAuth Client ID/Secret alınmış
- [ ] Email SMTP ayarları yapılmış
- [ ] Tüm testler geçiyor
- [ ] Security headers aktif

---

## 🟣 Heroku Deployment

### 1. Heroku Hazırlık

```bash
# Heroku CLI yükle (https://devcenter.heroku.com/articles/heroku-cli)
# Login
heroku login

# Yeni app oluştur
heroku create collectorium-prod --region eu

# PostgreSQL ekle
heroku addons:create heroku-postgresql:mini

# Redis ekle (opsiyonel - cache için)
heroku addons:create heroku-redis:mini
```

### 2. Environment Variables

```bash
# Production settings
heroku config:set DJANGO_ENV=prod
heroku config:set DJANGO_SETTINGS_MODULE=collectorium.settings.prod

# Security
heroku config:set SECRET_KEY=$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')
heroku config:set ALLOWED_HOSTS=collectorium-prod.herokuapp.com
heroku config:set CSRF_TRUSTED_ORIGINS=https://collectorium-prod.herokuapp.com

# Google OAuth
heroku config:set GOOGLE_CLIENT_ID=your-client-id
heroku config:set GOOGLE_CLIENT_SECRET=your-client-secret

# Email (Gmail örneği)
heroku config:set EMAIL_HOST=smtp.gmail.com
heroku config:set EMAIL_PORT=587
heroku config:set EMAIL_HOST_USER=your-email@gmail.com
heroku config:set EMAIL_HOST_PASSWORD=your-app-password
```

### 3. Procfile Oluştur

`Procfile` (root dizinde):

```
web: gunicorn collectorium.wsgi --log-file -
release: python manage.py migrate --noinput
```

### 4. runtime.txt Oluştur

`runtime.txt`:

```
python-3.11.0
```

### 5. Deploy

```bash
# Git remote ekle (eğer yoksa)
heroku git:remote -a collectorium-prod

# Deploy
git push heroku main

# Logs kontrol
heroku logs --tail

# Scale
heroku ps:scale web=1
```

### 6. Post-Deployment

```bash
# Superuser oluştur
heroku run python manage.py createsuperuser

# Fixture data yükle
heroku run python manage.py loaddata fixtures/categories.json

# Static files collect (otomatik olmalı)
heroku run python manage.py collectstatic --noinput

# Admin'e gir ve Google OAuth ayarlarını yap
# https://collectorium-prod.herokuapp.com/admin/
```

---

## 🔵 Railway Deployment

### 1. Railway Setup

```bash
# Railway CLI yükle
npm install -g @railway/cli

# Login
railway login

# Yeni proje
railway init
```

### 2. Railway Variables

Railway Dashboard'dan:

```
DJANGO_ENV=prod
DJANGO_SETTINGS_MODULE=collectorium.settings.prod
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=your-app.railway.app
# ... diğer environment variables
```

### 3. railway.json

```json
{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "gunicorn collectorium.wsgi:application",
    "healthcheckPath": "/healthz/",
    "restartPolicyType": "ON_FAILURE"
  }
}
```

### 4. Deploy

```bash
# Deploy
railway up

# Logs
railway logs
```

---

## 🟢 DigitalOcean App Platform

### 1. App Spec YAML

`.do/app.yaml`:

```yaml
name: collectorium
region: fra
services:
  - name: web
    github:
      repo: yourusername/collectorium
      branch: main
    build_command: pip install -r requirements.txt
    run_command: gunicorn collectorium.wsgi:application
    environment_slug: python
    instance_count: 1
    instance_size_slug: basic-xxs
    http_port: 8000
    routes:
      - path: /
    envs:
      - key: DJANGO_ENV
        value: "prod"
      - key: SECRET_KEY
        type: SECRET
databases:
  - name: db
    engine: PG
    version: "15"
```

---

## 🐳 Docker Deployment

### 1. Dockerfile

`infra/docker/Dockerfile`:

```dockerfile
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
WORKDIR /app

# Install dependencies
COPY pyproject.toml ./
RUN pip install --upgrade pip && \
    pip install -e .

# Copy project
COPY . .

# Collect static
RUN python manage.py collectstatic --noinput

# Run
CMD ["gunicorn", "collectorium.wsgi:application", "--bind", "0.0.0.0:8000"]
```

### 2. docker-compose.yml

```yaml
version: '3.8'

services:
  web:
    build: .
    command: gunicorn collectorium.wsgi:application --bind 0.0.0.0:8000
    volumes:
      - .:/app
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    ports:
      - "8000:8000"
    env_file:
      - .env.prod
    depends_on:
      - db
      - redis

  db:
    image: postgres:15
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB=collectorium
      - POSTGRES_USER=collectorium
      - POSTGRES_PASSWORD=changeme

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - static_volume:/app/staticfiles
      - media_volume:/app/media
      - ./infra/docker/nginx.conf:/etc/nginx/conf.d/default.conf
    depends_on:
      - web

volumes:
  postgres_data:
  redis_data:
  static_volume:
  media_volume:
```

### 3. Deploy

```bash
docker-compose up -d
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

---

## 🔒 Production Security Checklist

- [ ] HTTPS enforced (`SECURE_SSL_REDIRECT=True`)
- [ ] HSTS enabled
- [ ] Secure cookies (`SESSION_COOKIE_SECURE=True`)
- [ ] CSRF protection active
- [ ] SQL injection protection (Django ORM)
- [ ] XSS protection headers
- [ ] Admin panel IP restriction (opsiyonel)
- [ ] Rate limiting (django-ratelimit)
- [ ] Sentry error tracking
- [ ] Regular backups
- [ ] Security headers (django-csp)

---

## 📊 Monitoring & Logs

### Sentry Integration

```python
# settings/prod.py
import sentry_sdk

sentry_sdk.init(
    dsn=os.environ.get('SENTRY_DSN'),
    traces_sample_rate=0.1,
    environment='production',
)
```

### Application Monitoring

- **Heroku**: Heroku Metrics + Papertrail
- **Railway**: Built-in metrics
- **DigitalOcean**: App Platform Insights

---

## 🔄 CI/CD Pipeline (GitHub Actions)

`.github/workflows/deploy.yml`:

```yaml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install -e ".[test]"
      - run: pytest

  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: akhileshns/heroku-deploy@v3.12.14
        with:
          heroku_api_key: ${{secrets.HEROKU_API_KEY}}
          heroku_app_name: "collectorium-prod"
          heroku_email: "your-email@example.com"
```

---

## 🆘 Troubleshooting

### Static Files Yüklenmiyor

```bash
python manage.py collectstatic --noinput
# WhiteNoise middleware kontrol et
```

### Database Connection Error

```bash
# DATABASE_URL kontrol
echo $DATABASE_URL

# PostgreSQL bağlantı test
python manage.py dbshell
```

### 500 Internal Server Error

```bash
# Logs kontrol
heroku logs --tail

# Debug mode AÇMA, log level artır
heroku config:set LOG_LEVEL=DEBUG
```

---

**Deployment başarılı! 🎉**

