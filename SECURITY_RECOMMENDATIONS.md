# 🔐 Collectorium Security Recommendations

**Target Environment**: cPanel/Passenger Production  
**Last Updated**: October 20, 2025

---

## ⚠️ HIGH PRIORITY RECOMMENDATIONS

### 1. Change Admin URL (Recommended)

**Current**: `/admin/` (default, publicly known)  
**Recommendation**: Change to custom URL to prevent brute-force attacks

#### Option A: Environment Variable (Recommended)

**In `collectorium/settings/hosting.py`:**

```python
# Admin URL customization (add after imports)
ADMIN_URL = os.environ.get('ADMIN_URL', 'admin/').rstrip('/') + '/'
```

**In `collectorium/urls.py`:**

```python
from django.conf import settings

urlpatterns = [
    # Use custom admin URL from settings
    path(getattr(settings, 'ADMIN_URL', 'admin/'), admin.site.urls),
    # ... rest of patterns
]
```

**In cPanel Environment Variables:**

```
ADMIN_URL=control-panel-xj9k2/
```

Then restart application:
```bash
touch ~/collectorium/tmp/restart.txt
```

**New Admin URL**: `https://yourdomain.com/control-panel-xj9k2/`

#### Option B: Simple Direct Change

**In `collectorium/urls.py`:**

```python
urlpatterns = [
    path('control-panel/', admin.site.urls),  # Changed from 'admin/'
    # ... rest of patterns
]
```

**New Admin URL**: `https://yourdomain.com/control-panel/`

**Remember to:**
1. Update bookmarks
2. Update deployment scripts that reference `/admin/`
3. Document new URL in secure location

---

### 2. Rate Limiting (Recommended)

Install `django-ratelimit` to prevent brute-force attacks:

```bash
pip install django-ratelimit
```

**In `requirements.txt`:**
```
django-ratelimit>=4.1.0
```

**In login view** (e.g., `accounts/views.py`):

```python
from django_ratelimit.decorators import ratelimit

@ratelimit(key='ip', rate='5/h', method='POST')
def login_view(request):
    # Your login logic
    pass
```

---

### 3. Failed Login Monitoring

**Enable Django Admin Login Logging:**

Add to `collectorium/settings/hosting.py`:

```python
LOGGING['loggers']['django.security'] = {
    'handlers': ['file', 'console'],
    'level': 'WARNING',
    'propagate': False,
}
```

**Monitor failed logins:**

```bash
grep "login failed" ~/logs/django.log
```

---

### 4. Two-Factor Authentication (Optional but Recommended)

For additional security, consider:

- **django-otp**: Standard 2FA solution
- **django-allauth-2fa**: Integrates with django-allauth

```bash
pip install django-allauth-2fa
```

---

### 5. Database Password Rotation

**Schedule**: Every 90 days

**Procedure:**
1. Create new database password in cPanel
2. Update `DATABASE_URL` environment variable
3. Restart application: `touch tmp/restart.txt`
4. Test immediately

---

### 6. SECRET_KEY Rotation

**Schedule**: Every 6 months or if compromised

**Generate new key:**

```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

**Update in cPanel:**
1. Update `SECRET_KEY` environment variable
2. Restart application
3. **Note**: This will invalidate all active sessions

---

### 7. SSL/HTTPS Configuration

**Verify SSL certificate:**

```bash
python scripts/verify_ssl_ready.py yourdomain.com
```

**If SSL is ready:**

```bash
# In cPanel → Python App → Environment Variables
SECURE_SSL_REDIRECT=True
```

**If SSL is NOT ready yet:**

```bash
# Keep disabled temporarily
SECURE_SSL_REDIRECT=False
```

Once SSL is configured, enable redirect and restart.

---

### 8. File Upload Security

**Current settings** (in `hosting.py`):

```python
FILE_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10 MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10 MB
```

**Recommendations:**
- Validate file types in forms
- Scan uploaded files for malware (if handling user uploads)
- Consider external storage (S3, Cloudinary) for user-uploaded media

---

### 9. Dependency Security Updates

**Monthly security check:**

```bash
pip install safety
safety check -r requirements.txt
```

**Or use GitHub Dependabot:**
- Already configured in `.github/workflows/`
- Monitors vulnerabilities automatically
- Creates PRs for updates

---

### 10. Security Headers Verification

**Check headers:**

```bash
curl -I https://yourdomain.com | grep -i "security\|strict\|xss\|frame"
```

**Expected headers:**
- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: DENY`
- `X-XSS-Protection: 1; mode=block`
- `Strict-Transport-Security: max-age=31536000; includeSubDomains; preload`
- `Referrer-Policy: strict-origin-when-cross-origin`

---

## 🔍 SECURITY AUDIT CHECKLIST

### Pre-Production
- [ ] Changed admin URL from `/admin/`
- [ ] Enabled rate limiting on login
- [ ] Verified `DEBUG=False`
- [ ] Verified strong `SECRET_KEY` in environment
- [ ] Verified `ALLOWED_HOSTS` configured correctly
- [ ] Verified `CSRF_TRUSTED_ORIGINS` configured
- [ ] SSL certificate installed and verified
- [ ] `SECURE_SSL_REDIRECT=True` (after SSL ready)
- [ ] All security headers enabled
- [ ] File upload limits configured
- [ ] Sensitive files protected (.htaccess)
- [ ] Database password is strong (16+ characters)
- [ ] Email settings configured (for notifications)

### Post-Production
- [ ] Monitor logs daily for failed logins
- [ ] Set up external monitoring (UptimeRobot, etc.)
- [ ] Schedule monthly dependency updates
- [ ] Schedule quarterly security audits
- [ ] Set up automated backups
- [ ] Test backup restoration monthly
- [ ] Document incident response procedures

---

## 🚨 INCIDENT RESPONSE

### If Suspicious Activity Detected

1. **Immediate Actions:**
   ```bash
   # Check recent logins
   grep "login" ~/logs/django.log | tail -100
   
   # Check failed login attempts
   grep "failed" ~/logs/django.log | tail -50
   
   # Check admin access
   grep "admin" ~/logs/django.log | tail -50
   ```

2. **If Compromised:**
   - Immediately rotate `SECRET_KEY`
   - Reset admin passwords
   - Review and revoke suspicious sessions
   - Check for unauthorized database changes
   - Review file uploads for malicious content
   - Enable 2FA if not already enabled

3. **Contact:**
   - Hosting support: support@veridyen.com
   - Development team: your-team@example.com

---

## 📊 SECURITY MONITORING

### Daily
- Review error logs for security warnings
- Check failed login attempts

### Weekly
- Review all admin panel access
- Check for unusual database activity
- Verify SSL certificate status

### Monthly
- Run `safety check` on dependencies
- Review and update security settings
- Test backup restoration
- Audit user permissions

### Quarterly
- Full security audit
- Penetration testing (optional)
- Update security documentation
- Review incident response procedures

---

## 📚 RESOURCES

- [Django Security Docs](https://docs.djangoproject.com/en/stable/topics/security/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Django Security Checklist](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/)
- [cPanel Security Best Practices](https://docs.cpanel.net/knowledge-base/security/)

---

**Remember**: Security is an ongoing process, not a one-time setup.  
**Review and update this document quarterly.**

**Last Security Audit**: October 20, 2025  
**Next Scheduled Audit**: January 20, 2026


