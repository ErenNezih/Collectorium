# Collectorium cPanel Operations Runbook

**Version**: 1.0  
**Last Updated**: October 20, 2025  
**Environment**: cPanel/Passenger Production

---

## 📋 Table of Contents

- [Quick Reference](#quick-reference)
- [Application Management](#application-management)
- [Database Operations](#database-operations)
- [Static Files & Media](#static-files--media)
- [Logging & Monitoring](#logging--monitoring)
- [Troubleshooting](#troubleshooting)
- [Backup & Recovery](#backup--recovery)
- [Security Operations](#security-operations)
- [Performance Tuning](#performance-tuning)
- [Emergency Procedures](#emergency-procedures)

---

## 🚀 Quick Reference

### Essential Commands

```bash
# SSH into cPanel
ssh username@your-cpanel-host.com

# Navigate to project
cd ~/collectorium

# Activate virtual environment
source ~/virtualenv/collectorium/bin/activate

# Restart application
mkdir -p tmp && touch tmp/restart.txt

# View logs
tail -f logs/django.log
```

### Important Paths

| Path | Description |
|------|-------------|
| `~/collectorium/` | Application root |
| `~/virtualenv/collectorium/` | Virtual environment |
| `~/public/static/` | Static files (served by WhiteNoise) |
| `~/public/media/` | User-uploaded media |
| `~/logs/` | Application logs |
| `~/backups/` | Database backups |

### Key URLs

| URL | Purpose |
|-----|---------|
| `/healthz/` | Health check endpoint |
| `/admin/` | Django admin panel |
| `/` | Homepage |

---

## 🔧 Application Management

### Restart Application

**Method 1: Passenger Restart (Recommended)**

```bash
cd ~/collectorium
mkdir -p tmp
touch tmp/restart.txt
```

This triggers a zero-downtime restart. The application restarts when the next request arrives.

**Method 2: cPanel Python App Interface**

1. Log in to cPanel
2. Navigate to "Setup Python App"
3. Find "collectorium" app
4. Click "Restart" button

**Verification:**

```bash
# Check if application is responding
curl -I https://yourdomain.com/healthz/

# Should return HTTP/2 200
```

### Update Application Code

**Via Git (cPanel Git Interface):**

```bash
# In cPanel Git Version Control
1. Click "Pull or Deploy"
2. Select "Deploy HEAD Commit"
3. Application restarts automatically
```

**Via SSH/FTP:**

```bash
# Upload changed files
# Then:
cd ~/collectorium
source ~/virtualenv/collectorium/bin/activate
python manage.py collectstatic --noinput
mkdir -p tmp && touch tmp/restart.txt
```

### Update Dependencies

```bash
cd ~/collectorium
source ~/virtualenv/collectorium/bin/activate

# Update pip
pip install --upgrade pip

# Install/update requirements
pip install -r requirements.txt

# Restart application
touch tmp/restart.txt
```

### Run Migrations

```bash
cd ~/collectorium
source ~/virtualenv/collectorium/bin/activate

# Check migration status
python manage.py showmigrations

# Apply migrations
python manage.py migrate --noinput

# Restart application
touch tmp/restart.txt
```

---

## 🗄️ Database Operations

### Test Database Connection

```bash
cd ~/collectorium
source ~/virtualenv/collectorium/bin/activate

# Run test script
python scripts/test_db_connection.py
```

### Database Shell Access

**PostgreSQL:**

```bash
cd ~/collectorium
source ~/virtualenv/collectorium/bin/activate
python manage.py dbshell
```

Or direct psql:

```bash
psql -h hostname -U username -d database_name
```

**MySQL:**

```bash
mysql -h localhost -u username -p database_name
```

### Create Database Backup

```bash
cd ~/collectorium
source ~/virtualenv/collectorium/bin/activate

# Run backup script
python scripts/backup_database.py

# Backups stored in ~/backups/
```

### Restore Database Backup

**PostgreSQL:**

```bash
# Unzip backup
gunzip ~/backups/collectorium_YYYYMMDD_HHMMSS.sql.gz

# Restore
psql -h hostname -U username -d database_name < ~/backups/collectorium_YYYYMMDD_HHMMSS.sql
```

**MySQL:**

```bash
# Unzip backup
gunzip ~/backups/collectorium_YYYYMMDD_HHMMSS.sql.gz

# Restore
mysql -h localhost -u username -p database_name < ~/backups/collectorium_YYYYMMDD_HHMMSS.sql
```

### View Database Size

**PostgreSQL:**

```sql
SELECT pg_size_pretty(pg_database_size('database_name'));
```

**MySQL:**

```sql
SELECT 
    table_schema AS 'Database',
    ROUND(SUM(data_length + index_length) / 1024 / 1024, 2) AS 'Size (MB)'
FROM information_schema.tables
WHERE table_schema = 'database_name';
```

---

## 📁 Static Files & Media

### Collect Static Files

```bash
cd ~/collectorium
source ~/virtualenv/collectorium/bin/activate

# Collect static files
python manage.py collectstatic --noinput --clear

# Restart application
touch tmp/restart.txt
```

### Check Static Files Status

```bash
# Count static files
find ~/public/static -type f | wc -l

# Check permissions
ls -la ~/public/static

# Test static file access
curl -I https://yourdomain.com/static/admin/css/base.css
```

### Media Files Management

```bash
# Check media directory size
du -sh ~/public/media

# Count media files
find ~/public/media -type f | wc -l

# Set correct permissions (if needed)
chmod -R 755 ~/public/media
```

### Clear Static Files Cache

```bash
# Remove cached static files
rm -rf ~/public/static/*

# Recollect
cd ~/collectorium
source ~/virtualenv/collectorium/bin/activate
python manage.py collectstatic --noinput

# Restart
touch tmp/restart.txt
```

---

## 📊 Logging & Monitoring

### View Application Logs

**Real-time log monitoring:**

```bash
# Django application logs
tail -f ~/logs/django.log

# Error logs only
tail -f ~/logs/error.log

# Passenger logs (via cPanel)
# Navigate to: Setup Python App → View Logs
```

**Search logs:**

```bash
# Search for errors
grep -i error ~/logs/django.log | tail -20

# Search for specific pattern
grep "database connection" ~/logs/django.log

# Count occurrences
grep -c "ERROR" ~/logs/django.log
```

**Log rotation status:**

```bash
# Check log file sizes
ls -lh ~/logs/

# Manually rotate logs (if needed)
cd ~/logs
mv django.log django.log.$(date +%Y%m%d)
touch django.log
```

### Health Check

```bash
# Command-line health check
curl -s https://yourdomain.com/healthz/ | jq

# Expected response:
# {
#   "status": "healthy",
#   "database": "ok",
#   "django": "5.2.1",
#   "commit": "abc1234",
#   "debug": false
# }
```

### Application Status

```bash
# Check if application is running
curl -I https://yourdomain.com/

# Check Passenger status (via cPanel)
# Setup Python App → View metrics
```

### Performance Monitoring

```bash
# Check database connection count
# PostgreSQL:
SELECT count(*) FROM pg_stat_activity WHERE datname = 'database_name';

# MySQL:
SHOW PROCESSLIST;

# Check disk usage
df -h ~

# Check inode usage
df -i ~
```

---

## 🔍 Troubleshooting

### Application Not Starting

**Symptoms:** 503 error, "Application failed to start"

**Diagnosis:**

```bash
# Check Passenger error log (in cPanel → Python App → Logs)
# Common issues:
# 1. Syntax error in code
# 2. Missing dependencies
# 3. Environment variables not set
# 4. Database connection failure
```

**Solutions:**

```bash
# 1. Check passenger_wsgi.py exists and is valid
cat ~/collectorium/passenger_wsgi.py

# 2. Verify Python version in cPanel matches requirements
python --version

# 3. Reinstall dependencies
cd ~/collectorium
source ~/virtualenv/collectorium/bin/activate
pip install -r requirements.txt --force-reinstall

# 4. Check environment variables (cPanel → Python App → Environment)

# 5. Test Django settings
python manage.py check

# 6. Restart application
touch tmp/restart.txt
```

### Database Connection Errors

**Symptoms:** "database connection failed", 500 errors

**Diagnosis:**

```bash
# Test database connection
cd ~/collectorium
source ~/virtualenv/collectorium/bin/activate
python scripts/test_db_connection.py
```

**Solutions:**

```bash
# 1. Verify DATABASE_URL environment variable
echo $DATABASE_URL

# 2. Test database connectivity
# PostgreSQL:
psql -h hostname -U username -d database_name -c "SELECT 1"

# MySQL:
mysql -h localhost -u username -p -e "SELECT 1"

# 3. Check database credentials in cPanel environment variables

# 4. Verify database service is running (contact hosting support if external)

# 5. Check firewall rules (for external PostgreSQL)
```

### Static Files Not Loading

**Symptoms:** No CSS/JS, missing images

**Diagnosis:**

```bash
# Test static file access
curl -I https://yourdomain.com/static/admin/css/base.css

# Check static directory exists
ls -la ~/public/static
```

**Solutions:**

```bash
# 1. Recollect static files
cd ~/collectorium
source ~/virtualenv/collectorium/bin/activate
python manage.py collectstatic --noinput --clear

# 2. Check permissions
chmod -R 755 ~/public/static

# 3. Verify STATIC_ROOT in settings
python manage.py shell
>>> from django.conf import settings
>>> print(settings.STATIC_ROOT)

# 4. Check WhiteNoise is in MIDDLEWARE
grep -i whitenoise collectorium/settings/hosting.py

# 5. Restart application
touch tmp/restart.txt
```

### High Memory Usage

**Symptoms:** Application slow, 503 errors, "out of memory"

**Diagnosis:**

```bash
# Check memory usage (if available)
# Contact cPanel support for memory statistics
```

**Solutions:**

```bash
# 1. Restart application to clear memory
touch tmp/restart.txt

# 2. Review LOGGING settings to reduce verbosity

# 3. Check for memory leaks in custom code

# 4. Consider upgrading hosting plan for more resources

# 5. Optimize database queries
```

### 500 Internal Server Error

**Symptoms:** "500 Internal Server Error" on all pages

**Diagnosis:**

```bash
# Check error logs
tail -50 ~/logs/error.log

# Check Django log
tail -50 ~/logs/django.log
```

**Solutions:**

```bash
# 1. Verify DEBUG=False in production
cd ~/collectorium
source ~/virtualenv/collectorium/bin/activate
python manage.py shell
>>> from django.conf import settings
>>> print(settings.DEBUG)  # Should be False

# 2. Check ALLOWED_HOSTS setting
>>> print(settings.ALLOWED_HOSTS)

# 3. Run Django deployment check
python manage.py check --deploy

# 4. Review recent code changes

# 5. Rollback to previous working version if needed
```

### Email Not Sending

**Symptoms:** Password reset emails not received, no contact form emails

**Diagnosis:**

```bash
# Test email configuration
cd ~/collectorium
source ~/virtualenv/collectorium/bin/activate
python scripts/test_email.py your-email@example.com
```

**Solutions:**

```bash
# 1. Verify EMAIL_* environment variables

# 2. For Gmail, use App Password (not account password)

# 3. Check SMTP port is not blocked by firewall

# 4. For cPanel email, use localhost as EMAIL_HOST

# 5. Check spam folder for test emails
```

---

## 💾 Backup & Recovery

### Automated Backups

**Set up daily database backup cron job:**

```bash
# In cPanel → Cron Jobs, add:
# Daily at 2:00 AM:
0 2 * * * cd ~/collectorium && source ~/virtualenv/collectorium/bin/activate && python scripts/backup_database.py
```

**Backup schedule:**
- Database: Daily at 2:00 AM
- Backups retained: 30 days
- Location: `~/backups/`

### Manual Backup

```bash
# Full backup (database + media)
cd ~/collectorium
source ~/virtualenv/collectorium/bin/activate

# Backup database
python scripts/backup_database.py

# Backup media files
tar -czf ~/backups/media_$(date +%Y%m%d).tar.gz ~/public/media

# Backup configuration
cp .env ~/backups/.env.$(date +%Y%m%d).backup
```

### Recovery Procedures

**Full recovery:**

```bash
# 1. Restore database (see Database Operations)

# 2. Restore media files
cd ~
tar -xzf backups/media_YYYYMMDD.tar.gz -C ~/public/

# 3. Restore configuration
cp ~/backups/.env.YYYYMMDD.backup ~/collectorium/.env

# 4. Restart application
cd ~/collectorium
touch tmp/restart.txt
```

### Disaster Recovery

**If application is completely broken:**

```bash
# 1. Clone repository
cd ~
git clone https://github.com/yourusername/collectorium.git collectorium_new

# 2. Set up virtual environment
cd collectorium_new
virtualenv -p python3 ~/virtualenv/collectorium_new

# 3. Install dependencies
source ~/virtualenv/collectorium_new/bin/activate
pip install -r requirements.txt

# 4. Restore database
# (see Database Operations)

# 5. Configure environment variables

# 6. Collect static files
python manage.py collectstatic --noinput

# 7. Update cPanel Python App to point to new directory

# 8. Restart application
```

---

## 🔐 Security Operations

### Update Django SECRET_KEY

```bash
# Generate new secret key
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'

# Update in cPanel → Python App → Environment Variables
# Key: SECRET_KEY
# Value: [new secret key]

# Restart application
cd ~/collectorium
touch tmp/restart.txt

# Note: This will invalidate all sessions
```

### Create Superuser

```bash
cd ~/collectorium
source ~/virtualenv/collectorium/bin/activate

python manage.py createsuperuser

# Follow prompts for username, email, password
```

### Change User Password

```bash
cd ~/collectorium
source ~/virtualenv/collectorium/bin/activate

python manage.py changepassword username
```

### Review Failed Login Attempts

```bash
# Check logs for failed login attempts
grep -i "failed login" ~/logs/django.log | tail -20

# Check authentication errors
grep -i "authentication" ~/logs/error.log
```

### SSL Certificate Management

**In cPanel:**
1. Navigate to "SSL/TLS"
2. Use "AutoSSL" for automatic Let's Encrypt certificates
3. Ensure certificate is valid and auto-renewing

**Verify SSL:**

```bash
curl -vI https://yourdomain.com 2>&1 | grep -i ssl
```

---

## ⚡ Performance Tuning

### Database Query Optimization

```bash
# Enable query logging (temporarily)
# In collectorium/settings/hosting.py:
# LOGGING['loggers']['django.db.backends'] = {
#     'level': 'DEBUG',
#     'handlers': ['console'],
# }

# Review slow queries
grep -i "slow" ~/logs/django.log
```

### Cache Configuration

```bash
# If Redis is available, update environment variables:
# REDIS_URL=redis://localhost:6379/0

# Verify cache is working
cd ~/collectorium
source ~/virtualenv/collectorium/bin/activate
python manage.py shell
>>> from django.core.cache import cache
>>> cache.set('test', 'value', 60)
>>> print(cache.get('test'))  # Should print 'value'
```

### Static Files Optimization

```bash
# WhiteNoise automatically compresses and caches static files
# Verify compression is enabled
cd ~/collectorium
python manage.py shell
>>> from django.conf import settings
>>> print(settings.STATICFILES_STORAGE)
# Should be: whitenoise.storage.CompressedManifestStaticFilesStorage
```

---

## 🚨 Emergency Procedures

### Application Down - Quick Recovery

```bash
# 1. Restart application
cd ~/collectorium
mkdir -p tmp && touch tmp/restart.txt

# 2. Check health
curl -I https://yourdomain.com/healthz/

# 3. If still down, check logs
tail -50 ~/logs/error.log

# 4. If database issue, restart database connection
# Contact hosting support

# 5. If code issue, rollback to previous version
git log --oneline -10  # Find last working commit
git checkout COMMIT_HASH
touch tmp/restart.txt
```

### Database Emergency

```bash
# If database is down or corrupted

# 1. Attempt connection test
python scripts/test_db_connection.py

# 2. If external PostgreSQL, contact provider

# 3. If MySQL, check cPanel → MySQL Databases

# 4. Restore from latest backup
python scripts/backup_database.py  # First, backup current state
# Then restore from ~/backups/

# 5. Verify database integrity
# PostgreSQL: VACUUM ANALYZE;
# MySQL: CHECK TABLE table_name;
```

### Rollback Deployment

```bash
# Via Git
cd ~/collectorium
git log --oneline -10  # Find last working commit
git checkout COMMIT_HASH
touch tmp/restart.txt

# Via cPanel Git Interface
# 1. Navigate to Git Version Control
# 2. Find previous commit
# 3. Deploy that commit
```

### Emergency Contacts

- **Hosting Support**: support@veridyen.com (example)
- **Database Provider**: (if external)
- **DNS Provider**: (your domain registrar)
- **Development Team**: your-team@example.com

---

## 📝 Maintenance Schedule

### Daily
- ✅ Automated database backup (2:00 AM via cron)
- ✅ Check health endpoint
- ✅ Review error logs

### Weekly
- ✅ Review application logs for errors
- ✅ Check disk space usage
- ✅ Test backup restoration (monthly full test)
- ✅ Update dependencies (security patches)

### Monthly
- ✅ Full backup test (restore to staging)
- ✅ Review performance metrics
- ✅ Update Django and dependencies
- ✅ Security audit
- ✅ Review and clean up old logs/backups

### Quarterly
- ✅ Review and update documentation
- ✅ Disaster recovery drill
- ✅ Review and optimize database queries
- ✅ Review SSL certificate status

---

## 📚 Additional Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Passenger Documentation](https://www.phusionpassenger.com/docs/)
- [cPanel Documentation](https://docs.cpanel.net/)
- [Project Documentation](docs/)
- [Migration Guide](docs/MIGRATION_TO_CPANEL.md)

---

**Document Version**: 1.0  
**Last Reviewed**: October 20, 2025  
**Next Review**: January 20, 2026


