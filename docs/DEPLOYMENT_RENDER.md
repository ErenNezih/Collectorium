# 🚀 Render Deployment Guide

Bu proje Render.com üzerinde ücretsiz planda çalışacak şekilde yapılandırılmıştır.

## Komutlar

- Build Command: `bash ./build.sh`
- Start Command: `bash ./start.sh`

`build.sh` → pip install + collectstatic
`start.sh` → migrate + auto-superuser + gunicorn

## Ortam Değişkenleri

- `DJANGO_SETTINGS_MODULE=collectorium.settings.render`
- `DATABASE_URL` → Render Postgres (Internal Database URL veya “Link existing database”)
- `ALLOWED_HOSTS=<servis>.onrender.com`
- `SECRET_KEY` (generate)
- `DEBUG=False`
- `PYTHON_VERSION=3.12.3`
- (Opsiyonel) `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`

## Health Check

- `/healthz` 200 döner; JSON içinde `database`, `django`, `commit` değerleri bulunur
  - Render env otomatik `RENDER_GIT_COMMIT` sağlar

## Sorun Giderme

- Status 127 / collectstatic → Collectstatic sadece build’te olmalı
- DATABASE_URL eksik → DB’i servise bağlayın
- Template error (APP_DIRS + loaders) → `APP_DIRS=False` + cached loader (render.py)
- `cryptography` eksik → `requirements.txt` içinde mevcut

## Rollback

Render → Revisions → önceki başarılı build → Rollback.


