# 👨‍💻 Development Guide

## Kurulum

1) Python 3.12.3 kurun, repo’yu klonlayın, virtualenv oluşturun
2) `pip install -r requirements.txt`
3) `copy env.example .env` ve yerelde gerekli anahtarları doldurun
4) `python manage.py migrate && python manage.py createsuperuser`
5) `python manage.py runserver`

## Faydalı Komutlar

- Migrations: `python manage.py makemigrations && python manage.py migrate`
- Statikler: `python manage.py collectstatic --noinput`
- Health: `curl http://127.0.0.1:8000/healthz/`

## Kod Kalitesi

- PEP8/Black/Ruff tercihen kullanılabilir (opsiyonel)
- Anlamlı isimlendirme ve erken dönüş prensipleri

## OAuth (opsiyonel)

- Google Client ID/Secret .env’e eklenir
- Admin → Social applications → Google eklenir


