# 📗 COLLECTORIUM - OPERATIONS RUNBOOK

## Günlük Operasyonlar

### Sistem Sağlık Kontrolü

```bash
# Health endpoint kontrolü
curl https://your-domain.com/healthz

# Expected response:
# {"status": "healthy", "database": "ok", "cache": "ok"}
```

### Log Monitoring

```bash
# Heroku logs
heroku logs --tail --app collectorium-prod

# Filter by level
heroku logs --tail --source app | grep ERROR

# Last 100 lines
heroku logs -n 100 --app collectorium-prod
```

### Database Backup

```bash
# Heroku Postgres backup
heroku pg:backups:capture --app collectorium-prod

# Download backup
heroku pg:backups:download --app collectorium-prod

# List backups
heroku pg:backups --app collectorium-prod
```

## Sorun Giderme

### Application Down

1. **Health check**
   ```bash
   curl https://your-domain.com/healthz
   ```

2. **Logs kontrolü**
   ```bash
   heroku logs --tail
   ```

3. **Dyno restart**
   ```bash
   heroku restart --app collectorium-prod
   ```

### Yavaş Performans

1. **Database connections**
   ```bash
   heroku pg:info --app collectorium-prod
   ```

2. **Memory usage**
   ```bash
   heroku ps --app collectorium-prod
   ```

3. **Slow queries**
   - Django Debug Toolbar kullan (dev)
   - `django-silk` profiling ekle (staging)

### Static Files Yüklenmiyor

```bash
# Collectstatic çalıştır
heroku run python manage.py collectstatic --noinput

# WhiteNoise configuration kontrol
# settings.py → MIDDLEWARE'de WhiteNoiseMiddleware olmalı
```

## Deployment Checklist

### Pre-Deployment

- [ ] Tests geçiyor (`pytest`)
- [ ] Linting temiz (`ruff check`)
- [ ] Migrations hazır
- [ ] .env.example güncel
- [ ] CHANGELOG.md güncellendi

### Deployment

- [ ] Database backup alındı
- [ ] `git push heroku main`
- [ ] Migrations çalıştırıldı
- [ ] Static files collected
- [ ] Health check geçti

### Post-Deployment

- [ ] Kritik user journeys test edildi
- [ ] Error rate normal
- [ ] Response time normal
- [ ] Rollback planı hazır

## Maintenance Windows

### Scheduled Maintenance

```bash
# Enable maintenance mode (Heroku)
heroku maintenance:on --app collectorium-prod

# Perform maintenance tasks
heroku run python manage.py migrate
heroku run python manage.py some_command

# Disable maintenance mode
heroku maintenance:off --app collectorium-prod
```

### Emergency Rollback

```bash
# Heroku rollback
heroku releases --app collectorium-prod
heroku rollback v123 --app collectorium-prod

# Database rollback
heroku pg:backups:restore <backup-id> DATABASE_URL --app collectorium-prod
```

## Monitoring Alerts

### Critical Alerts (Immediate Response)

- Application down (>5 min)
- Database connection errors
- 500 error rate >5%
- Response time >3s (p95)

### Warning Alerts (Within 1 hour)

- Disk usage >80%
- Memory usage >85%
- 404 rate spike
- Failed background jobs

## Contact Information

- **On-Call Engineer:** [Your contact]
- **Infrastructure:** [Provider support]
- **Database:** [DBA contact]
- **Security:** [Security team]

