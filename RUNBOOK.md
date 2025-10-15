# 📘 COLLECTORIUM OPERATIONS RUNBOOK

**Version:** 1.0  
**Platform:** Render.com  
**Last Updated:** 2025-01-15

---

## 🎯 OVERVIEW

This runbook contains operational procedures for managing Collectorium on Render.com.

---

## 🚀 DEPLOYMENT

### Initial Deployment

1. **Push code to GitHub:**
   ```bash
   git add .
   git commit -m "feat: ready for production deployment"
   git push origin main
   ```

2. **Create Render account:**
   - Go to https://render.com
   - Sign up with GitHub

3. **Deploy using Blueprint:**
   - Dashboard → New → Blueprint
   - Select `Collectorium` repository
   - Render will auto-detect `render.yaml`
   - Click "Apply"
   - Wait 5-7 minutes for deployment

### Redeployment

**Automatic (Recommended):**
- Push to `main` branch
- Render auto-deploys within 1-2 minutes

**Manual:**
- Render Dashboard → Manual Deploy → Deploy latest commit

---

## 🔄 ROLLBACK PROCEDURES

### Quick Rollback (via Render Dashboard)

1. Navigate to Render Dashboard
2. Select `collectorium` service
3. Click "Deployments" tab
4. Find the last known good deployment
5. Click ⋮ (three dots) → "Rollback to this version"
6. Confirm rollback

**Time:** ~2-3 minutes

### Git-based Rollback

1. **Find the commit to revert to:**
   ```bash
   git log --oneline
   ```

2. **Revert to specific commit:**
   ```bash
   git revert <commit-hash>
   git push origin main
   ```

3. **Or reset (use with caution):**
   ```bash
   git reset --hard <commit-hash>
   git push origin main --force
   ```

---

## 🗄️ DATABASE MANAGEMENT

### Backup Database

**Via Render Dashboard:**
1. Dashboard → Select PostgreSQL service
2. Click "Backups" tab
3. Click "Create Manual Backup"

**Via pg_dump (if external access needed):**
```bash
# Get DATABASE_URL from Render Dashboard
pg_dump $DATABASE_URL > backup_$(date +%Y%m%d).sql
```

### Restore Database

1. Download backup file
2. Get DATABASE_URL from Render
3. Run:
   ```bash
   psql $DATABASE_URL < backup_file.sql
   ```

### Run Migrations Manually

**Via Render Shell:**
1. Dashboard → collectorium service → Shell tab
2. Run:
   ```bash
   python manage.py migrate
   ```

**Or via SSH (if configured):**
```bash
render ssh collectorium
python manage.py migrate
```

---

## 👤 USER MANAGEMENT

### Create Superuser Manually

1. Render Dashboard → Shell
2. Run:
   ```bash
   python manage.py createsuperuser
   ```

### Reset Superuser Password

1. Render Dashboard → Shell
2. Run:
   ```python
   python manage.py shell
   from django.contrib.auth import get_user_model
   User = get_user_model()
   user = User.objects.get(username='admin')
   user.set_password('new_password')
   user.save()
   exit()
   ```

---

## 📦 STATIC FILES

### Recollect Static Files

**If static files are not loading:**

1. Render Dashboard → Shell
2. Run:
   ```bash
   python manage.py collectstatic --noinput --clear
   ```

3. Restart service:
   - Dashboard → Settings → Manual Deploy → Deploy latest commit

---

## 🔧 ENVIRONMENT VARIABLES

### View Environment Variables

- Dashboard → collectorium service → Environment tab

### Add/Update Environment Variable

1. Dashboard → Environment tab
2. Click "Add Environment Variable"
3. Enter Key and Value
4. Click "Save Changes"
5. Service will auto-redeploy

### Critical Environment Variables

| Variable | Purpose | Example |
|----------|---------|---------|
| `DJANGO_SETTINGS_MODULE` | Settings file | `collectorium.settings.render` |
| `SECRET_KEY` | Django secret | Auto-generated |
| `DATABASE_URL` | PostgreSQL connection | Auto-provided |
| `DEBUG` | Debug mode | `False` |
| `DJANGO_SUPERUSER_USERNAME` | Admin username | `admin` |
| `DJANGO_SUPERUSER_PASSWORD` | Admin password | Auto-generated |

---

## 📊 MONITORING & LOGS

### View Logs

**Real-time:**
- Dashboard → Logs tab
- Auto-refreshes

**Download Logs:**
- Logs tab → Download

**Filter Logs:**
- Use search box in Logs tab

### Common Log Patterns

**Success:**
```
✅ Service is live
✅ Build completed successfully
✅ Deploy successful
```

**Errors:**
```
❌ ModuleNotFoundError: ...
❌ DatabaseError: ...
❌ Static files not found
```

---

## 🔍 HEALTH CHECKS

### Manual Health Check

**Browser:**
```
https://collectorium.onrender.com/healthz/
```

**curl:**
```bash
curl https://collectorium.onrender.com/healthz/
```

**Expected Response:**
```json
{
  "status": "healthy",
  "database": "ok",
  "version": "5.1.0",
  "debug": false
}
```

### Automated Health Checks

Render automatically monitors `/healthz/` endpoint:
- Interval: 30 seconds
- Timeout: 10 seconds
- Unhealthy threshold: 3 consecutive failures

---

## 🐛 TROUBLESHOOTING

### Service Won't Start

**Check:**
1. Logs for error messages
2. Environment variables are set
3. DATABASE_URL is correct
4. All migrations are applied

**Fix:**
```bash
# Via Shell
python manage.py check
python manage.py showmigrations
python manage.py migrate
```

### Database Connection Issues

**Symptoms:**
- 500 errors
- "OperationalError" in logs
- "connection refused"

**Solutions:**
1. Verify PostgreSQL service is running
2. Check DATABASE_URL format
3. Test connection:
   ```bash
   python manage.py dbshell
   ```

### Static Files 404

**Solutions:**
1. Run collectstatic:
   ```bash
   python manage.py collectstatic --noinput
   ```

2. Verify WhiteNoise in MIDDLEWARE (settings.py)

3. Check STATIC_ROOT and STATIC_URL

### Slow Performance

**Check:**
1. Database query performance
2. Gunicorn worker count
3. Memory usage in Render metrics

**Optimize:**
1. Add database indexes
2. Enable query caching
3. Upgrade to paid tier if needed

---

## 🔐 SECURITY

### Rotate SECRET_KEY

1. Generate new key:
   ```bash
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```

2. Update in Render Dashboard → Environment
3. Redeploy

### Update Dependencies

1. Update `requirements.txt`:
   ```bash
   pip list --outdated
   pip install -U <package>
   pip freeze > requirements.txt
   ```

2. Test locally
3. Push to GitHub
4. Auto-deploy

### SSL/HTTPS

- Automatically handled by Render
- HSTS enabled in settings.py
- Certificate auto-renews

---

## 📈 SCALING

### Vertical Scaling (Upgrade Plan)

1. Dashboard → Settings
2. Select higher tier plan
3. Confirm

### Horizontal Scaling

**Gunicorn Workers:**
- Edit `gunicorn.conf.py`
- Increase `workers` value
- Push to GitHub

**Database:**
- Upgrade PostgreSQL plan in Render Dashboard

---

## 🎯 COMMON TASKS

### Run Django Management Command

```bash
# Via Render Shell
python manage.py <command>

# Examples:
python manage.py shell
python manage.py dbshell
python manage.py check
python manage.py showmigrations
```

### Clear Cache (if Redis configured)

```bash
python manage.py shell
from django.core.cache import cache
cache.clear()
```

### Export Data

```bash
python manage.py dumpdata > data.json
```

### Import Data

```bash
python manage.py loaddata data.json
```

---

## 📞 SUPPORT & ESCALATION

**Render Support:**
- Dashboard → Help & Support
- Documentation: https://render.com/docs
- Community: https://community.render.com

**Django Support:**
- Documentation: https://docs.djangoproject.com
- Forum: https://forum.djangoproject.com

**Emergency Contacts:**
- Project Owner: [Your Email]
- DevOps Team: [Team Email/Slack]

---

## 📝 CHANGE LOG

| Date | Change | Author |
|------|--------|--------|
| 2025-01-15 | Initial deployment | Cursor AI |
| - | - | - |

---

**END OF RUNBOOK**

