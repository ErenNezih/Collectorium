# 🚀 cPanel Git Push Deployment Sistemi

## 🎯 Amaç
Local'deki değişiklikleri `git push` ile cPanel'e otomatik deploy etmek.

## 📋 Kurulum Adımları

### 1. cPanel'de Git Repository Kurulumu

**cPanel → Git Version Control → Create Repository**

1. **Repository Name**: `collectorium`
2. **Clone URL**: `https://github.com/KULLANICI_ADINIZ/collectorium.git`
3. **Repository Path**: `/home/collecto/collectorium`
4. **Branch**: `main`

### 2. GitHub Repository Hazırlığı

```bash
# Local'de GitHub'a push
git add .
git commit -m "cPanel deployment ready"
git push origin main
```

### 3. cPanel Auto-Deploy Ayarları

**Git Version Control → collectorium → Settings**

1. **Auto-Deploy**: ✅ Enabled
2. **Branch**: `main`
3. **Deploy Commands**: 
   ```bash
   source /home/collecto/virtualenv/collectorium/3.12/bin/activate
   cd /home/collecto/collectorium
   pip install -r requirements.txt
   python manage.py migrate --noinput
   python manage.py collectstatic --noinput
   touch tmp/restart.txt
   ```

### 4. Webhook Kurulumu (Opsiyonel)

**GitHub → Repository → Settings → Webhooks**

- **Payload URL**: `https://collectorium.com.tr/cpanel-webhook/`
- **Content Type**: `application/json`
- **Events**: `Push`

## 🔄 Deployment Workflow

### Normal Kullanım:
```bash
# Local'de değişiklik yap
git add .
git commit -m "Feature: new feature"
git push origin main

# cPanel otomatik deploy eder (2-3 dakika)
```

### Manuel Deploy:
```bash
# cPanel → Git Version Control → collectorium → Deploy
```

## 🛠️ Troubleshooting

### Problem 1: Permission Hatası
```bash
# cPanel Terminal'de:
chmod 755 /home/collecto/collectorium
chown -R collecto:collecto /home/collecto/collectorium
```

### Problem 2: Virtual Environment
```bash
# .cpanel.yml güncelle:
deployment:
  tasks:
    - source /home/collecto/virtualenv/collectorium/3.12/bin/activate
    - cd /home/collecto/collectorium
    - pip install -r requirements.txt
    - python manage.py migrate --noinput
    - python manage.py collectstatic --noinput
    - touch tmp/restart.txt
```

### Problem 3: Database Migration
```bash
# Environment variables kontrol:
echo $DB_ENGINE
echo $DB_NAME
echo $DB_USER
```

## ✅ Test Etme

```bash
# 1. Local'de değişiklik yap
echo "test" >> test.txt
git add test.txt
git commit -m "test deployment"
git push origin main

# 2. cPanel'de kontrol et
# File Manager → collectorium → test.txt var mı?

# 3. Site'yi kontrol et
# https://collectorium.com.tr/healthz
```

## 🚨 Güvenlik

- **Environment variables** cPanel'de ayarlanmış ✅
- **SECRET_KEY** güvenli ✅
- **Database credentials** korunuyor ✅

## 📞 Destek

Sorun olursa:
1. cPanel → Git Version Control → Logs
2. cPanel → Terminal → Error messages
3. File Manager → logs/ klasörü
