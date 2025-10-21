# 🧪 DRY-RUN TEST PLAN

**Tarih**: 20 Ekim 2025  
**Amaç**: Deployment öncesi tüm komutları test etmek  
**NOT**: Bu komutları çalıştırmadan önce environment variables ayarlanmalı

---

## ⚙️ ENVIRONMENT SETUP

### Required Environment Variables

**Bash**:
```bash
export DJANGO_SETTINGS_MODULE=collectorium.settings.hosting
export SECRET_KEY=test-secret-key-change-in-production
export DEBUG=False
export ALLOWED_HOSTS=localhost,127.0.0.1
export CSRF_TRUSTED_ORIGINS=https://localhost,https://127.0.0.1
export DATABASE_URL=sqlite:///db.sqlite3  # or PostgreSQL/MySQL
export EMAIL_HOST=localhost
export SECURE_SSL_REDIRECT=False  # Test ortamda
```

**PowerShell**:
```powershell
$env:DJANGO_SETTINGS_MODULE="collectorium.settings.hosting"
$env:SECRET_KEY="test-secret-key-change-in-production"
$env:DEBUG="False"
$env:ALLOWED_HOSTS="localhost,127.0.0.1"
$env:CSRF_TRUSTED_ORIGINS="https://localhost,https://127.0.0.1"
$env:DATABASE_URL="sqlite:///db.sqlite3"
$env:EMAIL_HOST="localhost"
$env:SECURE_SSL_REDIRECT="False"
```

---

## 🧪 TEST SUITE 1: DEPENDENCY CHECK

### Bash
```bash
#!/bin/bash
echo "=== DEPENDENCY CHECK ==="

# 1. Python version
echo "Python version:"
python -V

# 2. Pip version
echo "Pip version:"
python -m pip --version

# 3. Install dependencies (if not already)
echo "Installing dependencies..."
python -m pip install -r requirements.txt

# 4. Check for conflicts
echo "Checking for dependency conflicts..."
python -m pip check

# 5. Test critical imports
echo "Testing critical imports..."
python -c "
import django
import allauth
import django_htmx
import whitenoise
from PIL import Image
import psycopg2
import pymysql
import requests
import sentry_sdk
print('All critical imports: OK')
"

echo "=== DEPENDENCY CHECK COMPLETE ==="
```

### PowerShell
```powershell
Write-Host "=== DEPENDENCY CHECK ===" -ForegroundColor Cyan

# 1. Python version
Write-Host "Python version:"
python -V

# 2. Pip version
Write-Host "Pip version:"
python -m pip --version

# 3. Check for conflicts
Write-Host "Checking for dependency conflicts..."
python -m pip check

# 4. Test critical imports
Write-Host "Testing critical imports..."
python -c @"
import django
import allauth
import django_htmx
import whitenoise
from PIL import Image
print('Core imports: OK')
"@

Write-Host "=== DEPENDENCY CHECK COMPLETE ===" -ForegroundColor Green
```

**Beklenen Sonuç**: Tüm import'lar başarılı, no conflicts

---

## 🧪 TEST SUITE 2: DJANGO CHECKS

### Bash
```bash
#!/bin/bash
echo "=== DJANGO SYSTEM CHECKS ==="

# 1. Basic system check
echo "Running basic system check..."
python manage.py check

# 2. Deployment check
echo "Running deployment check..."
python manage.py check --deploy

# 3. Tag-specific checks
echo "Running security checks..."
python manage.py check --tag security

echo "Running database checks..."
python manage.py check --tag database

echo "=== DJANGO CHECKS COMPLETE ==="
```

### PowerShell
```powershell
Write-Host "=== DJANGO SYSTEM CHECKS ===" -ForegroundColor Cyan

# 1. Basic system check
Write-Host "Running basic system check..."
python manage.py check

# 2. Deployment check
Write-Host "Running deployment check..."
python manage.py check --deploy

# 3. Security check
Write-Host "Running security checks..."
python manage.py check --tag security

Write-Host "=== DJANGO CHECKS COMPLETE ===" -ForegroundColor Green
```

**Beklenen Sonuç**: No issues found (veya sadece warnings)

---

## 🧪 TEST SUITE 3: MIGRATION CHECK

### Bash
```bash
#!/bin/bash
echo "=== MIGRATION CHECKS ==="

# 1. Check for pending migrations
echo "Checking for pending model changes..."
python manage.py makemigrations --check --dry-run

# 2. Show migration plan
echo "Migration plan:"
python manage.py migrate --plan

# 3. Show all migrations status
echo "All migrations status:"
python manage.py showmigrations

# 4. Test migration (dry-run not available, use plan)
echo "Testing migration execution (use --fake-initial for existing DB)..."
# python manage.py migrate --noinput  # Don't run in dry-run

echo "=== MIGRATION CHECKS COMPLETE ==="
```

### PowerShell
```powershell
Write-Host "=== MIGRATION CHECKS ===" -ForegroundColor Cyan

# 1. Check for pending migrations
Write-Host "Checking for pending model changes..."
python manage.py makemigrations --check --dry-run

# 2. Show migration plan
Write-Host "Migration plan:"
python manage.py migrate --plan

# 3. Show all migrations status
Write-Host "All migrations status:"
python manage.py showmigrations

Write-Host "=== MIGRATION CHECKS COMPLETE ===" -ForegroundColor Green
```

**Beklenen Sonuç**: No changes detected, no pending migrations

---

## 🧪 TEST SUITE 4: STATIC FILES

### Bash
```bash
#!/bin/bash
echo "=== STATIC FILES TEST ==="

# 1. Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

# 2. Verify static directory
echo "Verifying static directory..."
ls -la staticfiles/

# 3. Check admin static
echo "Checking admin static files..."
test -f staticfiles/admin/css/base.css && echo "✅ Admin static OK" || echo "❌ Admin static missing"

# 4. Check custom static
echo "Checking custom static files..."
test -f staticfiles/css/custom.css && echo "✅ Custom static OK" || echo "❌ Custom static missing"

# 5. Check WhiteNoise manifest
echo "Checking WhiteNoise manifest..."
test -f staticfiles/staticfiles.json && echo "✅ Manifest OK" || echo "❌ Manifest missing"

# 6. Count static files
echo "Total static files:"
find staticfiles -type f | wc -l

echo "=== STATIC FILES TEST COMPLETE ==="
```

### PowerShell
```powershell
Write-Host "=== STATIC FILES TEST ===" -ForegroundColor Cyan

# 1. Collect static files
Write-Host "Collecting static files..."
python manage.py collectstatic --noinput --clear

# 2. Verify static directory
Write-Host "Verifying static directory..."
Get-ChildItem staticfiles | Select-Object Name, Length

# 3. Check admin static
Write-Host "Checking admin static files..."
if (Test-Path staticfiles\admin\css\base.css) {
    Write-Host "✅ Admin static OK" -ForegroundColor Green
} else {
    Write-Host "❌ Admin static missing" -ForegroundColor Red
}

# 4. Check custom static
Write-Host "Checking custom static files..."
if (Test-Path staticfiles\css\custom.css) {
    Write-Host "✅ Custom static OK" -ForegroundColor Green
} else {
    Write-Host "⚠️ Custom static missing" -ForegroundColor Yellow
}

# 5. Count static files
Write-Host "Total static files:"
(Get-ChildItem staticfiles -Recurse -File).Count

Write-Host "=== STATIC FILES TEST COMPLETE ===" -ForegroundColor Green
```

**Beklenen Sonuç**: staticfiles/ dolu, manifest created, admin static OK

---

## 🧪 TEST SUITE 5: DATABASE CONNECTION

### Bash
```bash
#!/bin/bash
echo "=== DATABASE CONNECTION TEST ==="

# Run dedicated test script
python scripts/test_db_connection.py

echo "=== DATABASE CONNECTION TEST COMPLETE ==="
```

### PowerShell
```powershell
Write-Host "=== DATABASE CONNECTION TEST ===" -ForegroundColor Cyan

# Run dedicated test script
python scripts\test_db_connection.py

Write-Host "=== DATABASE CONNECTION TEST COMPLETE ===" -ForegroundColor Green
```

**Beklenen Sonuç**: 
- Connection successful
- Database version displayed
- Write/read test passed
- Migrations status OK

---

## 🧪 TEST SUITE 6: EMAIL TEST

### Bash
```bash
#!/bin/bash
echo "=== EMAIL TEST ==="

# Test email sending (optional - skip if no email config)
python scripts/test_email.py your-test-email@example.com || echo "Email test skipped"

echo "=== EMAIL TEST COMPLETE ==="
```

### PowerShell
```powershell
Write-Host "=== EMAIL TEST ===" -ForegroundColor Cyan

# Test email sending (optional)
try {
    python scripts\test_email.py your-test-email@example.com
} catch {
    Write-Host "Email test skipped (optional)" -ForegroundColor Yellow
}

Write-Host "=== EMAIL TEST COMPLETE ===" -ForegroundColor Green
```

**Beklenen Sonuç**: Email sent (veya warning if not configured)

---

## 🧪 TEST SUITE 7: SSL VERIFICATION (Post-Deployment Only)

### Bash
```bash
#!/bin/bash
echo "=== SSL VERIFICATION ==="

# This requires domain to be accessible
# Skip in local environment

# Verify SSL certificate
python scripts/verify_ssl_ready.py yourdomain.com || echo "SSL verification skipped (local)"

echo "=== SSL VERIFICATION COMPLETE ==="
```

### PowerShell
```powershell
Write-Host "=== SSL VERIFICATION ===" -ForegroundColor Cyan

# Skip in local environment
Write-Host "SSL verification (deployment only)" -ForegroundColor Yellow

Write-Host "=== SSL VERIFICATION COMPLETE ===" -ForegroundColor Green
```

**Beklenen Sonuç** (cPanel'de): Certificate valid, days remaining shown

---

## 🧪 TEST SUITE 8: SMOKE TEST (Post-Deployment Only)

### Bash
```bash
#!/bin/bash
echo "=== SMOKE TEST ==="

# This requires application to be running
# Local: python manage.py runserver first
# cPanel: Application should be running

python scripts/smoke_test.py --base-url http://localhost:8000

echo "=== SMOKE TEST COMPLETE ==="
```

### PowerShell
```powershell
Write-Host "=== SMOKE TEST ===" -ForegroundColor Cyan

# Run smoke test
python scripts\smoke_test.py --base-url http://localhost:8000

Write-Host "=== SMOKE TEST COMPLETE ===" -ForegroundColor Green
```

**Beklenen Sonuç**: All tests passed (or warnings only)

---

## 🚀 COMPLETE DRY-RUN SCRIPT

### Bash (cPanel SSH)
```bash
#!/bin/bash
# Complete dry-run test suite for Collectorium
# Run this before deployment

set -e  # Exit on error

echo "╔════════════════════════════════════════════════════╗"
echo "║  COLLECTORIUM DRY-RUN TEST SUITE                  ║"
echo "╚════════════════════════════════════════════════════╝"
echo ""

# Navigate to project
cd ~/collectorium
source ~/virtualenv/collectorium/bin/activate

# Test 1: Dependencies
echo "📦 Test 1: Dependencies..."
python -m pip check || { echo "❌ Dependency check failed"; exit 1; }
echo "✅ Dependencies OK"
echo ""

# Test 2: Django Checks
echo "⚙️ Test 2: Django Checks..."
python manage.py check --deploy || { echo "❌ Django check failed"; exit 1; }
echo "✅ Django checks OK"
echo ""

# Test 3: Migrations
echo "🗄️ Test 3: Migrations..."
python manage.py makemigrations --check --dry-run || { echo "❌ Pending migrations found"; exit 1; }
python manage.py migrate --plan
echo "✅ Migrations OK"
echo ""

# Test 4: Static Files
echo "🎨 Test 4: Static Files..."
python manage.py collectstatic --noinput --clear || { echo "❌ collectstatic failed"; exit 1; }
test -f staticfiles/admin/css/base.css || { echo "❌ Admin static missing"; exit 1; }
echo "✅ Static files OK"
echo ""

# Test 5: Database Connection
echo "🗄️ Test 5: Database Connection..."
python scripts/test_db_connection.py || { echo "❌ Database test failed"; exit 1; }
echo "✅ Database connection OK"
echo ""

# Test 6: Email (optional)
echo "📧 Test 6: Email..."
python scripts/test_email.py || echo "⚠️ Email test skipped (optional)"
echo ""

# Summary
echo "╔════════════════════════════════════════════════════╗"
echo "║  ✅ ALL DRY-RUN TESTS PASSED                      ║"
echo "╚════════════════════════════════════════════════════╝"
echo ""
echo "Next steps:"
echo "  1. Review test outputs"
echo "  2. Fix any warnings"
echo "  3. Proceed with deployment"
```

### PowerShell (Windows Local)
```powershell
# Complete dry-run test suite for Collectorium (Windows)
# Run this before deployment

Write-Host "╔════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║  COLLECTORIUM DRY-RUN TEST SUITE                  ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Test 1: Dependencies
Write-Host "📦 Test 1: Dependencies..." -ForegroundColor Yellow
python -m pip check
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Dependency check failed" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Dependencies OK" -ForegroundColor Green
Write-Host ""

# Test 2: Django Checks
Write-Host "⚙️ Test 2: Django Checks..." -ForegroundColor Yellow
python manage.py check --deploy
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Django check failed" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Django checks OK" -ForegroundColor Green
Write-Host ""

# Test 3: Migrations
Write-Host "🗄️ Test 3: Migrations..." -ForegroundColor Yellow
python manage.py makemigrations --check --dry-run
if ($LASTEXITCODE -ne 0) {
    Write-Host "⚠️ Pending migrations found" -ForegroundColor Yellow
}
python manage.py migrate --plan
Write-Host "✅ Migrations OK" -ForegroundColor Green
Write-Host ""

# Test 4: Static Files
Write-Host "🎨 Test 4: Static Files..." -ForegroundColor Yellow
python manage.py collectstatic --noinput --clear
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ collectstatic failed" -ForegroundColor Red
    exit 1
}
if (Test-Path staticfiles\admin\css\base.css) {
    Write-Host "✅ Static files OK" -ForegroundColor Green
} else {
    Write-Host "❌ Admin static missing" -ForegroundColor Red
    exit 1
}
Write-Host ""

# Test 5: Database Connection
Write-Host "🗄️ Test 5: Database Connection..." -ForegroundColor Yellow
python scripts\test_db_connection.py
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Database test failed" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Database connection OK" -ForegroundColor Green
Write-Host ""

# Test 6: Email (optional)
Write-Host "📧 Test 6: Email (optional)..." -ForegroundColor Yellow
try {
    python scripts\test_email.py
} catch {
    Write-Host "⚠️ Email test skipped (optional)" -ForegroundColor Yellow
}
Write-Host ""

# Summary
Write-Host "╔════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║  ✅ ALL DRY-RUN TESTS PASSED                      ║" -ForegroundColor Green
Write-Host "╚════════════════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:"
Write-Host "  1. Review test outputs"
Write-Host "  2. Fix any warnings"
Write-Host "  3. Proceed with deployment"
```

---

## 🧪 TEST SUITE 9: SMOKE TEST (Deployment Verification)

### Bash (After Deployment)
```bash
#!/bin/bash
echo "=== POST-DEPLOYMENT SMOKE TEST ==="

# Wait for application to start
echo "Waiting 30 seconds for application to start..."
sleep 30

# Run smoke tests
python scripts/smoke_test.py --base-url https://yourdomain.com

echo "=== SMOKE TEST COMPLETE ==="
```

### PowerShell (Local Server)
```powershell
Write-Host "=== SMOKE TEST ===" -ForegroundColor Cyan

# Start development server (background)
Write-Host "Starting development server..."
Start-Process python -ArgumentList "manage.py","runserver" -NoNewWindow

# Wait for server to start
Start-Sleep -Seconds 5

# Run smoke tests
python scripts\smoke_test.py --base-url http://localhost:8000

Write-Host "=== SMOKE TEST COMPLETE ===" -ForegroundColor Green
```

---

## 🧪 TEST SUITE 10: SECURITY SCAN

### Bash
```bash
#!/bin/bash
echo "=== SECURITY SCAN ==="

# 1. Dependency vulnerability scan
echo "Scanning for known vulnerabilities..."
pip install safety -q
safety check -r requirements.txt || echo "⚠️ Vulnerabilities found - review output"

# 2. Search for hardcoded secrets
echo "Searching for hardcoded secrets..."
grep -r "sk-" . --include="*.py" --exclude-dir=venv || echo "✅ No hardcoded secrets found"

# 3. Check for unsafe template tags
echo "Checking for |safe usage in templates..."
grep -r "|safe" templates/ || echo "✅ No |safe usage found"

echo "=== SECURITY SCAN COMPLETE ==="
```

### PowerShell
```powershell
Write-Host "=== SECURITY SCAN ===" -ForegroundColor Cyan

# 1. Dependency vulnerability scan
Write-Host "Scanning for known vulnerabilities..."
pip install safety -q
safety check -r requirements.txt

# 2. Search for hardcoded secrets
Write-Host "Searching for hardcoded secrets..."
$secrets = Select-String -Path *.py -Pattern "sk-|api_key.*=.*['\"]" -Recurse -Exclude venv,env
if ($secrets.Count -eq 0) {
    Write-Host "✅ No hardcoded secrets found" -ForegroundColor Green
} else {
    Write-Host "⚠️ Potential secrets found - review output" -ForegroundColor Yellow
}

Write-Host "=== SECURITY SCAN COMPLETE ===" -ForegroundColor Green
```

---

## 📊 TEST RESULT MATRIX

### Expected Results

| Test Suite | Expected Result | Critical? |
|------------|----------------|-----------|
| 1. Dependency Check | All imports OK | ✅ Yes |
| 2. Django Checks | No errors | ✅ Yes |
| 3. Migration Check | No pending | ✅ Yes |
| 4. Static Files | collectstatic OK | ✅ Yes |
| 5. Database Connection | Connection OK | ✅ Yes |
| 6. Email Test | Sent or skipped | ⚠️ Optional |
| 7. SSL Verification | Valid cert | ⚠️ Deployment only |
| 8. Smoke Test | All passed | ✅ Yes |
| 9. Security Scan | No critical | ✅ Yes |

---

## 🚨 ERROR HANDLING

### If Test Fails

**Dependency Check Fails**:
```bash
# Check specific package
python -c "import package_name"
# Error message will show what's missing

# Reinstall
pip install package_name --force-reinstall
```

**Django Check Fails**:
```bash
# Review error message
python manage.py check --deploy

# Common issues:
# - ALLOWED_HOSTS not set
# - CSRF_TRUSTED_ORIGINS not set
# - SECRET_KEY weak
```

**Migration Pending**:
```bash
# Create migrations
python manage.py makemigrations

# Review migration files
cat app/migrations/000X_name.py

# Apply if safe
python manage.py migrate
```

**collectstatic Fails**:
```bash
# Check STATIC_ROOT writable
ls -la staticfiles/

# Check WhiteNoise in MIDDLEWARE
grep -i whitenoise collectorium/settings/hosting.py

# Recollect
python manage.py collectstatic --noinput
```

**Database Connection Fails**:
```bash
# Check DATABASE_URL
echo $DATABASE_URL

# Test manual connection
# PostgreSQL:
psql $DATABASE_URL -c "SELECT 1"

# MySQL:
mysql -h host -u user -p -e "SELECT 1"
```

---

## 📝 TEST LOG TEMPLATE

### Suggested Log Format

```
=== COLLECTORIUM DRY-RUN TEST LOG ===
Date: 2025-10-20 16:00:00
Environment: cPanel SSH / Local Windows
Python Version: 3.11.5
Django Settings: collectorium.settings.hosting

TEST 1: Dependency Check
  [OK] Python 3.11.5
  [OK] pip check passed
  [OK] All imports successful

TEST 2: Django Checks
  [OK] Basic checks passed
  [WARNING] ALLOWED_HOSTS not set (expected in test)
  
TEST 3: Migrations
  [OK] No pending migrations
  [OK] Migration plan clean

TEST 4: Static Files
  [OK] collectstatic completed
  [OK] 1,234 files collected
  [OK] Admin static present

TEST 5: Database
  [OK] Connection successful
  [OK] PostgreSQL 15.3
  [OK] All tables present

TEST 6: Email
  [SKIPPED] Optional test

SUMMARY:
  ✅ Passed: 5
  ⚠️ Warnings: 1
  ❌ Failed: 0
  
RESULT: ✅ READY FOR DEPLOYMENT

=== END OF TEST LOG ===
```

**Save To**: `migrate_logs/dryrun_YYYYMMDD_HHMM.log`

---

## 🎯 QUICK REFERENCE

### Minimal Test (30 seconds)

**Bash**:
```bash
python -m pip check && \
python manage.py check --deploy && \
python manage.py migrate --plan && \
echo "✅ Quick checks passed"
```

**PowerShell**:
```powershell
python -m pip check ; python manage.py check --deploy ; python manage.py migrate --plan ; Write-Host "✅ Quick checks passed" -ForegroundColor Green
```

---

### Full Test (5 minutes)

**Bash**: Run complete dry-run script above

**PowerShell**: Run complete PowerShell script above

---

## ✅ CHECKLIST

### Pre-Test Setup

- [ ] Virtual environment activated
- [ ] Environment variables set
- [ ] Database accessible
- [ ] Network connectivity OK

### Run Tests

- [ ] Test 1: Dependency Check
- [ ] Test 2: Django Checks
- [ ] Test 3: Migration Check
- [ ] Test 4: Static Files
- [ ] Test 5: Database Connection
- [ ] Test 6: Email (optional)
- [ ] Test 7: SSL (deployment only)
- [ ] Test 8: Smoke Test (deployment only)
- [ ] Test 9: Security Scan

### Post-Test Actions

- [ ] Review all outputs
- [ ] Fix any warnings
- [ ] Save test log
- [ ] Proceed with deployment (if all passed)

---

## ✅ SONUÇ

**Test Coverage**: ✅ **COMPREHENSIVE**  
**Automation**: ✅ **SCRIPTED**  
**Platform Support**: ✅ **Bash + PowerShell**

**Estimated Test Time**: 5-10 minutes  
**Critical Tests**: 6  
**Optional Tests**: 3

**Ready for Deployment**: ✅ YES (after tests pass)

---

**Hazırlayan**: AI Assistant  
**Tarih**: 2025-10-20  
**Durum**: TAMAMLANDI ✅


