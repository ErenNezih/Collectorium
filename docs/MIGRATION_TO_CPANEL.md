# Collectorium Migration: Render.com → cPanel/Passenger WSGI

## 📋 Overview

This document details the complete migration of Collectorium from Render.com to Veridyen cPanel hosting environment using CloudLinux + Passenger WSGI.

**Migration Date**: October 20, 2025  
**Target Environment**: cPanel Shared Hosting (CloudLinux + Passenger)  
**Database Strategy**: PostgreSQL (external) or MySQL (cPanel)  
**Deployment Strategy**: Blue-Green (parallel setup, DNS cutover)

---

## 🎯 Migration Objectives

- **Zero Business Logic Changes**: No functional modifications
- **Clean Architecture**: Remove all Render-specific configurations
- **Production-Ready**: Security, performance, and operational best practices
- **Rollback Ready**: Render environment untouched until DNS cutover
- **Full Documentation**: Every step logged and reproducible

---

## 📦 Pre-Migration Checklist

### Current Render Environment
- [ ] Document current environment variables
- [ ] Export database backup (`pg_dump` or Render dashboard)
- [ ] Archive current `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS`
- [ ] Note all third-party service credentials (Google OAuth, SMTP, etc.)
- [ ] Record current static/media file structure
- [ ] Screenshot working health check: `/healthz`

### cPanel Environment Setup
- [ ] cPanel login credentials confirmed
- [ ] Python version available (3.8+)
- [ ] Database service decided (PostgreSQL external OR MySQL cPanel)
- [ ] SSL certificate ready (AutoSSL or manual)
- [ ] Storage quota checked for media files
- [ ] Domain DNS TTL reduced to 300s

---

## 🗺️ Migration Steps

### Step 0: Repository Preparation

**Files Created:**
- `docs/MIGRATION_TO_CPANEL.md` (this file)
- `migrate_logs/` directory for operation logs
- `passenger_wsgi.py` for cPanel/Passenger
- `collectorium/settings/hosting.py` for cPanel-specific settings
- `.cpanel.yml` for Git-based deployment
- `RUNBOOK_CPANEL.md` for operations

**Log**: `migrate_logs/00_repo_prep.log`

---

### Step 1: Render Cleanup

**Objective**: Remove all Render-specific files and configurations

#### Files to Delete/Disable:
```bash
# Render-specific deployment files
rm -f build.sh
rm -f start.sh
rm -f railway.json
rm -f .do/app.yaml
rm -f render.yaml
# Heroku files (if any)
rm -f Procfile
rm -f runtime.txt
```

#### Settings Cleanup:
- Remove `collectorium/settings/render.py` (if exists)
- Update `collectorium/settings/__init__.py` to not reference Render
- Remove Render environment variable checks in settings

#### Documentation Updates:
- Archive `docs/DEPLOYMENT_RENDER.md` → `docs/archive/`
- Update `DOCUMENTATION_INDEX.md` to reference cPanel deployment
- Remove Render references from `README.md`

#### Health Check Updates:
- Make `RENDER_GIT_COMMIT` and similar env vars optional in health checks
- Update `/healthz` to work without Render-specific metadata

**Validation**:
```bash
grep -r "render" collectorium/settings/ --ignore-case
grep -r "RENDER" . --include="*.py" --exclude-dir=venv
```

**Log**: `migrate_logs/01_render_cleanup.log`

---

### Step 2: cPanel/Passenger Integration

#### 2.1 Create `passenger_wsgi.py`

Create at project root:
```python
import os
import sys

# Add project directory to path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, CURRENT_DIR)

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'collectorium.settings.hosting')

# Get WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

#### 2.2 cPanel Python App Configuration

**In cPanel → Setup Python App:**
1. **Python Version**: 3.11 or latest available
2. **Application Root**: `/home/username/collectorium`
3. **Application URL**: `/` (or subdomain)
4. **Application Startup File**: `passenger_wsgi.py`
5. **Application Entry Point**: `application`

#### 2.3 Virtual Environment Setup

```bash
# SSH into cPanel
cd ~/collectorium
source /home/username/virtualenv/collectorium/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Verify installations
pip check
```

#### 2.4 Passenger Configuration File

Create `.htaccess` in public directory if needed:
```apache
PassengerEnabled On
PassengerAppRoot /home/username/collectorium
```

**Log**: `migrate_logs/02_cpanel_integration.log`

---

### Step 3: Settings Configuration

#### 3.1 Create `collectorium/settings/hosting.py`

```python
"""
cPanel/Passenger Production Settings
"""
from .base import *
import os

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Allowed hosts
ALLOWED_HOSTS = [
    'yourdomain.com',
    'www.yourdomain.com',
]

# CSRF trusted origins
CSRF_TRUSTED_ORIGINS = [
    'https://yourdomain.com',
    'https://www.yourdomain.com',
]

# Security settings
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# HSTS settings
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Database - see Step 4 for configuration
DATABASES = {
    'default': {
        'ENGINE': os.environ.get('DB_ENGINE', 'django.db.backends.postgresql'),
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT', '5432'),
        'OPTIONS': {
            'sslmode': 'require',
        } if os.environ.get('DB_ENGINE') == 'django.db.backends.postgresql' else {
            'charset': 'utf8mb4',
        }
    }
}

# Static files (WhiteNoise)
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATIC_ROOT = os.path.join(BASE_DIR.parent.parent, 'public', 'static')
STATIC_URL = '/static/'

# Media files
MEDIA_ROOT = os.path.join(BASE_DIR.parent.parent, 'public', 'media')
MEDIA_URL = '/media/'

# Email configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL')

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR.parent.parent, 'logs', 'django.log'),
            'formatter': 'verbose',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'INFO',
    },
}

# Admin URL (optionally obfuscate)
# ADMIN_URL = 'super-secret-admin/'  # Update urls.py if using this

# Google OAuth (if used)
# SOCIALACCOUNT_PROVIDERS settings remain same as base
```

#### 3.2 Environment Variables

Create `.env` file (or use cPanel environment variables):
```bash
# Django
SECRET_KEY=your-strong-secret-key-here
DJANGO_SETTINGS_MODULE=collectorium.settings.hosting

# Database
DB_ENGINE=django.db.backends.postgresql
DB_NAME=collectorium_db
DB_USER=dbuser
DB_PASSWORD=strong-password
DB_HOST=external-postgres-host.com
DB_PORT=5432

# Email
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@yourdomain.com

# Google OAuth (if used)
GOOGLE_OAUTH_CLIENT_ID=your-client-id
GOOGLE_OAUTH_CLIENT_SECRET=your-client-secret

# Sentry (optional)
SENTRY_DSN=your-sentry-dsn
```

**cPanel Environment Variables** (in Python App settings):
- Add all variables from `.env` to cPanel's environment variable manager

**Log**: `migrate_logs/03_settings_config.log`

---

### Step 4: Database Configuration

#### Decision Tree

**Option A: PostgreSQL (Recommended)**

External PostgreSQL service (VPS, Render DB, DigitalOcean, etc.)

**Pros:**
- No schema changes needed
- Minimal migration effort
- Keep existing data structure

**Steps:**
1. Set up external PostgreSQL instance
2. Configure firewall to allow cPanel server IP
3. Update `hosting.py` with connection details
4. Test connection: `python manage.py dbshell`
5. Migrate data if new instance:
   ```bash
   # On Render
   pg_dump DATABASE_URL > render_backup.sql
   
   # On new PostgreSQL
   psql NEW_DATABASE_URL < render_backup.sql
   ```

**Option B: MySQL (cPanel Native)**

Use cPanel's MySQL database

**Pros:**
- Native to cPanel
- No external dependencies
- Usually included in hosting

**Cons:**
- Schema compatibility review needed
- Data migration required
- Some PostgreSQL-specific features may need adjustment

**Steps:**
1. Create MySQL database in cPanel
2. Update `requirements.txt`: Add `mysqlclient`
3. Update `hosting.py`:
   ```python
   'ENGINE': 'django.db.backends.mysql',
   'OPTIONS': {
       'charset': 'utf8mb4',
       'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
   }
   ```
4. Data migration:
   ```bash
   # Export from Render (PostgreSQL)
   python manage.py dumpdata --natural-foreign --natural-primary --exclude auth.permission --exclude contenttypes > render_data.json
   
   # Import to cPanel (MySQL)
   python manage.py migrate
   python manage.py loaddata render_data.json
   ```
5. Test compatibility:
   ```bash
   python manage.py check
   python manage.py migrate --plan
   ```

#### Connection Testing

Create `scripts/test_db_connection.py`:
```python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'collectorium.settings.hosting')
django.setup()

from django.db import connection

try:
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        if result == (1,):
            print("✅ Database connection successful!")
        else:
            print("❌ Unexpected result")
except Exception as e:
    print(f"❌ Database connection failed: {e}")
```

Run: `python scripts/test_db_connection.py`

**Log**: `migrate_logs/04_database_setup.log`

---

### Step 5: Static & Media Files

#### 5.1 Directory Structure

```
/home/username/
├── collectorium/          # Django project
│   ├── manage.py
│   ├── passenger_wsgi.py
│   └── ...
├── public/                # Web-accessible files
│   ├── static/           # Collected static files
│   └── media/            # User uploads
└── logs/                 # Application logs
    └── django.log
```

#### 5.2 Collect Static Files

```bash
cd ~/collectorium
source /home/username/virtualenv/collectorium/bin/activate
python manage.py collectstatic --noinput
```

#### 5.3 Configure Static/Media Serving

**WhiteNoise** (already configured in settings):
- Serves static files directly from Django
- Works with Passenger/Apache

**Media Files** `.htaccess` in `public/media/`:
```apache
<Files "*">
    Order Allow,Deny
    Allow from all
</Files>
```

#### 5.4 Test Static Files

```bash
# Test a known static file
curl -I https://yourdomain.com/static/css/base.css

# Should return 200 OK
```

**Log**: `migrate_logs/05_static_media.log`

---

### Step 6: Security, Email & OAuth

#### 6.1 Security Checklist

```bash
# Run Django deployment check
python manage.py check --deploy

# Expected: No issues found
```

**Manual Verification:**
- [ ] `DEBUG = False`
- [ ] Strong `SECRET_KEY` in environment
- [ ] `ALLOWED_HOSTS` configured
- [ ] `CSRF_TRUSTED_ORIGINS` configured
- [ ] SSL redirect enabled
- [ ] HSTS headers configured
- [ ] Secure cookies enabled

#### 6.2 Email Testing

Create `scripts/test_email.py`:
```python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'collectorium.settings.hosting')
django.setup()

from django.core.mail import send_mail

try:
    send_mail(
        'Collectorium Test Email',
        'This is a test email from cPanel deployment.',
        'noreply@yourdomain.com',
        ['your-test-email@example.com'],
        fail_silently=False,
    )
    print("✅ Email sent successfully!")
except Exception as e:
    print(f"❌ Email failed: {e}")
```

Run: `python scripts/test_email.py`

#### 6.3 Google OAuth Configuration

1. **Google Cloud Console:**
   - Add new authorized redirect URI: `https://yourdomain.com/accounts/google/login/callback/`
   - Keep Render URI temporarily for rollback

2. **Django Admin:**
   - Log into `/admin/`
   - Navigate to `Sites` → Update domain to `yourdomain.com`
   - Navigate to `Social Applications` → Update or create Google provider
   - Add Client ID and Secret from cPanel environment

3. **Test OAuth Flow:**
   - Visit `/accounts/login/`
   - Click "Sign in with Google"
   - Complete authentication
   - Verify successful login

**Log**: `migrate_logs/06_security_email_oauth.log`

---

### Step 7: CI/CD Pipeline (Optional)

#### 7.1 GitHub Actions Deployment

Create `.github/workflows/deploy-cpanel.yml`:

```yaml
name: Deploy to cPanel

on:
  push:
    branches: [ main ]
  workflow_dispatch:

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v3
    
    - name: Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    
    - name: Run tests
      run: |
        python manage.py test --settings=collectorium.settings.test
    
    - name: Deploy to cPanel via FTP
      uses: SamKirkland/FTP-Deploy-Action@4.3.3
      with:
        server: ${{ secrets.CPANEL_FTP_HOST }}
        username: ${{ secrets.CPANEL_FTP_USER }}
        password: ${{ secrets.CPANEL_FTP_PASSWORD }}
        server-dir: /home/username/collectorium/
        exclude: |
          **/.git*
          **/.git*/**
          **/venv/**
          **/db.sqlite3
          **/__pycache__/**
          **/migrate_logs/**
    
    - name: Restart application
      uses: appleboy/ssh-action@v0.1.7
      with:
        host: ${{ secrets.CPANEL_SSH_HOST }}
        username: ${{ secrets.CPANEL_SSH_USER }}
        key: ${{ secrets.CPANEL_SSH_KEY }}
        script: |
          cd ~/collectorium
          source ~/virtualenv/collectorium/bin/activate
          python manage.py migrate --noinput
          python manage.py collectstatic --noinput
          mkdir -p tmp
          touch tmp/restart.txt
```

#### 7.2 Alternative: cPanel Git Version Control

1. **In cPanel:**
   - Navigate to "Git Version Control"
   - Click "Create"
   - Add repository URL: `https://github.com/yourusername/collectorium.git`
   - Set branch: `main`
   - Set deployment path: `/home/username/collectorium`

2. **Deploy Script** (`.cpanel.yml`):
```yaml
---
deployment:
  tasks:
    - export DEPLOYPATH=/home/username/collectorium
    - /bin/cp -R * $DEPLOYPATH
    - cd $DEPLOYPATH
    - source /home/username/virtualenv/collectorium/bin/activate
    - pip install -r requirements.txt
    - python manage.py migrate --noinput
    - python manage.py collectstatic --noinput
    - mkdir -p tmp
    - touch tmp/restart.txt
```

**Log**: `migrate_logs/07_cicd_setup.log`

---

### Step 8: Smoke Testing & Validation

#### 8.1 Create Smoke Test Script

`scripts/smoke_test.py`:
```python
#!/usr/bin/env python
"""
Comprehensive smoke test for cPanel deployment
"""
import sys
import requests
from colorama import init, Fore, Style

init(autoreset=True)

BASE_URL = "https://yourdomain.com"
TESTS = []

def test(name):
    def decorator(func):
        TESTS.append((name, func))
        return func
    return decorator

@test("Health check endpoint")
def test_health():
    response = requests.get(f"{BASE_URL}/healthz", timeout=10)
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    data = response.json()
    assert data.get('status') == 'ok', "Health check status not ok"
    assert data.get('database') == 'ok', "Database not healthy"
    return "✅ Health check passed"

@test("Admin login page")
def test_admin():
    response = requests.get(f"{BASE_URL}/admin/", timeout=10)
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    assert "Django" in response.text, "Admin page not rendering"
    return "✅ Admin accessible"

@test("Static files")
def test_static():
    # Test a known static file
    response = requests.head(f"{BASE_URL}/static/css/base.css", timeout=10)
    assert response.status_code == 200, f"Static file returned {response.status_code}"
    return "✅ Static files serving"

@test("Homepage")
def test_homepage():
    response = requests.get(f"{BASE_URL}/", timeout=10)
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    return "✅ Homepage loading"

@test("SSL/HTTPS")
def test_ssl():
    response = requests.get(f"{BASE_URL}/", timeout=10)
    assert response.url.startswith("https://"), "Not redirecting to HTTPS"
    return "✅ SSL redirect working"

def run_tests():
    print(f"{Fore.CYAN}{'='*60}")
    print(f"{Fore.CYAN}Collectorium cPanel Smoke Test")
    print(f"{Fore.CYAN}{'='*60}\n")
    
    passed = 0
    failed = 0
    
    for name, test_func in TESTS:
        try:
            print(f"{Fore.YELLOW}Testing: {name}...", end=" ")
            result = test_func()
            print(f"{Fore.GREEN}{result}")
            passed += 1
        except Exception as e:
            print(f"{Fore.RED}❌ FAILED: {str(e)}")
            failed += 1
    
    print(f"\n{Fore.CYAN}{'='*60}")
    print(f"{Fore.GREEN}Passed: {passed}")
    print(f"{Fore.RED}Failed: {failed}")
    print(f"{Fore.CYAN}{'='*60}\n")
    
    return failed == 0

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
```

#### 8.2 Manual Testing Checklist

- [ ] **Health Check**: Visit `/healthz` - expect 200 + JSON
- [ ] **Admin Panel**: 
  - [ ] Login at `/admin/`
  - [ ] Create/edit a Category
  - [ ] Create/edit a Listing
  - [ ] View user list
- [ ] **Static Files**:
  - [ ] Open browser DevTools → Network
  - [ ] Reload homepage
  - [ ] Verify CSS/JS files return 200
- [ ] **Media Upload**:
  - [ ] Upload a listing image
  - [ ] Verify image displays
  - [ ] Check file exists in `public/media/`
- [ ] **OAuth** (if enabled):
  - [ ] Click "Sign in with Google"
  - [ ] Complete authentication
  - [ ] Verify login successful
- [ ] **Email**:
  - [ ] Trigger password reset
  - [ ] Check email received
- [ ] **SSL**:
  - [ ] Visit `http://yourdomain.com`
  - [ ] Verify redirect to `https://`
  - [ ] Check browser shows secure lock icon

#### 8.3 Automated Validation Commands

```bash
# 1. Dependency check
python -m pip check

# 2. Django deployment check
python manage.py check --deploy

# 3. Migration status
python manage.py migrate --plan

# 4. Health check
curl -sS https://yourdomain.com/healthz | jq

# 5. Static file checks
curl -I https://yourdomain.com/static/admin/css/base.css
curl -I https://yourdomain.com/static/css/base.css

# 6. SSL/HTTPS redirect
curl -I http://yourdomain.com | grep -i location
```

**Log**: `migrate_logs/08_smoke_tests.log`

---

### Step 9: Cutover Plan (DNS Switch)

#### 9.1 Pre-Cutover Checklist

- [ ] All smoke tests passing
- [ ] Database backup completed
- [ ] Static/media files verified
- [ ] SSL certificate active on cPanel
- [ ] Environment variables configured
- [ ] Email sending confirmed
- [ ] OAuth configured (if used)
- [ ] Rollback plan documented

#### 9.2 DNS Preparation

**48 hours before cutover:**
```bash
# Reduce TTL to 5 minutes for fast propagation
# Update DNS records in your domain registrar:
# - A record TTL: 300 seconds
# - Wait 48 hours for old TTL to expire
```

#### 9.3 Cutover Procedure

**T-0 (Cutover moment):**

1. **Update DNS A Record:**
   ```
   yourdomain.com     A     300    [cPanel IP address]
   www.yourdomain.com A     300    [cPanel IP address]
   ```

2. **Monitor DNS Propagation:**
   ```bash
   # Check from multiple locations
   dig +short yourdomain.com
   
   # Online tools:
   # - whatsmydns.net
   # - dnschecker.org
   ```

3. **Watch Application Logs:**
   ```bash
   # SSH into cPanel
   tail -f ~/logs/django.log
   
   # Watch Passenger logs
   tail -f ~/logs/passenger.log
   ```

4. **Monitor Key Metrics (T+0 to T+30 minutes):**
   - Response times: Should be < 500ms
   - Error rate: Should be < 1%
   - Health check: Continuous 200 responses
   - Traffic volume: Should match previous baseline

5. **Test from Multiple Locations:**
   ```bash
   # Different geographic locations
   # Different ISPs
   # Mobile networks
   ```

#### 9.4 Post-Cutover Monitoring

**First Hour:**
- Monitor error logs every 5 minutes
- Check health endpoint every minute
- Verify user-facing features (login, browse, search)
- Watch for email alerts (if monitoring configured)

**First 24 Hours:**
- Review full error logs
- Check database performance
- Monitor disk space
- Verify scheduled tasks running (if any)

**First Week:**
- Daily log reviews
- Performance baseline establishment
- User feedback collection

**Log**: `migrate_logs/09_cutover.log`

---

### Step 10: Rollback Plan

#### 10.1 Rollback Triggers

Execute rollback if ANY of these occur within first hour:
- Health check fails consistently (> 3 failures in 5 minutes)
- Error rate > 5%
- Critical feature broken (auth, checkout, search)
- Database connection issues
- SSL certificate problems

#### 10.2 Rollback Procedure

**Total Time: < 10 minutes**

1. **Revert DNS (Fastest):**
   ```bash
   # Update A records back to Render IP
   yourdomain.com     A     300    [Render IP address]
   www.yourdomain.com A     300    [Render IP address]
   ```

2. **Verify Render Environment:**
   ```bash
   # Check Render is still responding
   curl https://collectorium.onrender.com/healthz
   ```

3. **Communicate:**
   - Notify team
   - Update status page (if applicable)
   - Document failure reason

4. **Post-Rollback:**
   - Investigate cPanel issues
   - Fix problems in staging
   - Re-test before second attempt

#### 10.3 Data Consistency

**If database diverged during cutover:**

```bash
# 1. Stop cPanel application
touch ~/collectorium/tmp/restart.txt

# 2. Identify delta transactions (if any)
# - Check timestamps
# - Identify new records created during cutover

# 3. Manual data sync if needed
# - Export delta from cPanel MySQL/PostgreSQL
# - Import to Render database

# 4. Resume Render
# DNS already pointing back
```

#### 10.4 Rollback Notes Document

Create `migrate_logs/rollback_notes.md`:
```markdown
# Rollback Execution Log

**Date**: [Date]
**Time**: [Time]
**Duration**: [Minutes]
**Trigger**: [Reason for rollback]

## Actions Taken
1. [Action 1]
2. [Action 2]
...

## Data Impact
- [Description of any data divergence]
- [Steps taken to reconcile]

## Root Cause
[Analysis of what went wrong]

## Next Steps
[Plan for second migration attempt]
```

**Log**: `migrate_logs/10_rollback_plan.log`

---

### Step 11: Operations & Maintenance

#### 11.1 Create `RUNBOOK_CPANEL.md`

See separate `RUNBOOK_CPANEL.md` file for detailed operational procedures.

**Key Sections:**
- Application Restart
- Log Viewing
- Database Operations
- Static Files Update
- Django Migrations
- Backup & Restore
- Performance Monitoring
- Troubleshooting Common Issues

#### 11.2 Backup Strategy

**Daily Database Backup** (cron job):
```bash
# Add to cPanel cron jobs
# Schedule: Daily at 2 AM
0 2 * * * cd ~/collectorium && source ~/virtualenv/collectorium/bin/activate && python scripts/backup_database.py
```

Create `scripts/backup_database.py`:
```python
import os
import django
from datetime import datetime
import subprocess

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'collectorium.settings.hosting')
django.setup()

from django.conf import settings

BACKUP_DIR = os.path.expanduser('~/backups')
os.makedirs(BACKUP_DIR, exist_ok=True)

timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
backup_file = f"{BACKUP_DIR}/collectorium_{timestamp}.sql"

db_config = settings.DATABASES['default']

if db_config['ENGINE'] == 'django.db.backends.postgresql':
    cmd = f"PGPASSWORD='{db_config['PASSWORD']}' pg_dump -h {db_config['HOST']} -U {db_config['USER']} -d {db_config['NAME']} > {backup_file}"
elif db_config['ENGINE'] == 'django.db.backends.mysql':
    cmd = f"mysqldump -h {db_config['HOST']} -u {db_config['USER']} -p'{db_config['PASSWORD']}' {db_config['NAME']} > {backup_file}"
else:
    print("Unsupported database engine")
    exit(1)

try:
    subprocess.run(cmd, shell=True, check=True)
    print(f"Backup successful: {backup_file}")
    
    # Compress backup
    subprocess.run(f"gzip {backup_file}", shell=True, check=True)
    print(f"Compressed: {backup_file}.gz")
    
    # Remove backups older than 30 days
    subprocess.run(f"find {BACKUP_DIR} -name '*.gz' -mtime +30 -delete", shell=True)
    
except Exception as e:
    print(f"Backup failed: {e}")
    exit(1)
```

#### 11.3 Uptime Monitoring

**External Monitoring Services:**
- UptimeRobot (free tier)
- Pingdom
- StatusCake
- Freshping

**Configuration:**
- Monitor URL: `https://yourdomain.com/healthz`
- Interval: 5 minutes
- Alert email: your-email@example.com
- Keyword check: `"status": "ok"`

#### 11.4 Log Rotation

Create `.htaccess` or configure in cPanel:
```apache
# Prevent direct access to logs
<Files "*.log">
    Order Allow,Deny
    Deny from all
</Files>
```

**Logrotate Configuration** (if cPanel supports):
```
/home/username/logs/*.log {
    daily
    rotate 30
    compress
    delaycompress
    notifempty
    missingok
}
```

**Log**: `migrate_logs/11_operations_setup.log`

---

## 📊 Migration Checklist Summary

### Pre-Migration
- [ ] Render environment documented
- [ ] Database backup completed
- [ ] Environment variables recorded
- [ ] cPanel account set up
- [ ] SSL certificate ready
- [ ] DNS TTL reduced

### Repository Changes
- [ ] `passenger_wsgi.py` created
- [ ] `collectorium/settings/hosting.py` created
- [ ] Render-specific files removed
- [ ] Documentation updated
- [ ] `.cpanel.yml` created (if using Git deploy)

### cPanel Configuration
- [ ] Python app configured
- [ ] Virtual environment created
- [ ] Dependencies installed
- [ ] Environment variables set
- [ ] Database configured
- [ ] Static files collected
- [ ] Media directory configured

### Security & Services
- [ ] Django deployment check passed
- [ ] Email sending tested
- [ ] OAuth configured (if used)
- [ ] SSL certificate active
- [ ] Security headers configured

### Testing
- [ ] Smoke tests passed
- [ ] Manual testing completed
- [ ] Health check responding
- [ ] Admin panel accessible
- [ ] Static files serving
- [ ] Media upload working

### Cutover
- [ ] DNS A record updated
- [ ] Propagation monitored
- [ ] Application monitored
- [ ] Logs reviewed
- [ ] Rollback plan ready

### Post-Migration
- [ ] 24-hour monitoring completed
- [ ] Backup cron configured
- [ ] Uptime monitoring active
- [ ] Operations runbook finalized
- [ ] Team trained on new environment

---

## 📞 Support & Escalation

### Common Issues

**Issue**: Application won't start after restart
- **Check**: Passenger error logs in cPanel
- **Check**: `passenger_wsgi.py` syntax
- **Check**: Virtual environment activated
- **Check**: All dependencies installed

**Issue**: Database connection fails
- **Check**: Environment variables set correctly
- **Check**: Database host reachable from cPanel
- **Check**: Firewall rules allow connection
- **Check**: Credentials are correct

**Issue**: Static files not loading
- **Check**: `collectstatic` ran successfully
- **Check**: `STATIC_ROOT` path correct
- **Check**: WhiteNoise in `INSTALLED_APPS`
- **Check**: File permissions (755 for dirs, 644 for files)

**Issue**: 500 errors on production
- **Check**: `DEBUG = False` is set
- **Check**: `ALLOWED_HOSTS` includes domain
- **Check**: Error logs in `~/logs/django.log`
- **Check**: Passenger logs in cPanel

### Escalation Contacts

- **cPanel Support**: support@veridyen.com (example)
- **Database Provider**: (if external PostgreSQL)
- **DNS Provider**: (domain registrar)
- **Development Team**: your-team@example.com

---

## 📚 Additional Resources

- [Passenger Documentation](https://www.phusionpassenger.com/docs/tutorials/fundamental_concepts/)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/)
- [cPanel Python App Documentation](https://docs.cpanel.net/knowledge-base/web-services/guide-to-python/)
- [WhiteNoise Documentation](http://whitenoise.evans.io/)

---

## 📝 Migration Log Files

All migration operations are logged in `migrate_logs/`:
- `00_repo_prep.log`
- `01_render_cleanup.log`
- `02_cpanel_integration.log`
- `03_settings_config.log`
- `04_database_setup.log`
- `05_static_media.log`
- `06_security_email_oauth.log`
- `07_cicd_setup.log`
- `08_smoke_tests.log`
- `09_cutover.log`
- `10_rollback_plan.log`
- `11_operations_setup.log`

---

**Document Version**: 1.0  
**Last Updated**: October 20, 2025  
**Author**: Migration Team  
**Status**: Ready for execution


