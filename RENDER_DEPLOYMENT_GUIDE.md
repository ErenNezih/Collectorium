# 🎨 COLLECTORIUM - RENDER.COM DEPLOYMENT GUIDE

**TAK TAK TAK! Adım adım Render deployment rehberi** 🚀

---

## ✅ HAZIRLIK TAMAMLANDI

Projeniz Render için tamamen hazır:

- ✅ `render.yaml` - Render blueprint
- ✅ `build.sh` - Build script
- ✅ `collectorium/settings/render.py` - Production settings
- ✅ `requirements.txt` - Dependencies
- ✅ Tüm mevcut kodunuz **AYNEN KORUNDU**

---

## 🚀 DEPLOYMENT ADIMLARI

### ADIM 1: GITHUB'A PUSH EDİN

PowerShell'de (proje klasöründe):

```powershell
git add .
git commit -m "Render deployment ready"
git push
```

**Durum:** GitHub'da güncel kodunuz olmalı ✅

---

### ADIM 2: RENDER.COM'A GİRİN

1. **https://render.com** → Sign up / Log in
2. **GitHub ile bağlanın** (Sign up with GitHub)
3. **Authorize Render** → Render'a GitHub erişimi verin

**Durum:** Render hesabınız hazır ✅

---

### ADIM 3: YENİ WEB SERVICE OLUŞTURUN

1. **Dashboard → "New +"** butonuna tıklayın
2. **"Blueprint"** seçeneğini seçin
3. **"Collectorium"** repository'sini seçin
4. Render `render.yaml` dosyasını otomatik algılayacak
5. **"Apply"** butonuna tıklayın

**ÖNEMLİ:** Blueprint otomatik olarak:
- Web service oluşturur
- PostgreSQL database oluşturur
- Her ikisini birbirine bağlar

**Durum:** Otomatik setup başladı ✅

---

### ADIM 4: DEPLOY'U İZLEYİN

Render otomatik olarak:

```
1. ✅ Repository'yi clone eder
2. ✅ Python 3.11 kurar
3. ✅ Dependencies yükler (pip install)
4. ✅ PostgreSQL database oluşturur
5. ✅ Migrations çalıştırır
6. ✅ Static files toplar
7. ✅ Gunicorn başlatır
8. 🎉 DEPLOY TAMAMLANDI!
```

**Süre:** 5-10 dakika

**Durum:** Canlıdasınız! ✅

---

### ADIM 5: SİTENİZİ AÇIN

Deploy tamamlanınca Render size URL verecek:

```
https://collectorium.onrender.com
```

**Test edin:**
- Ana sayfa
- Admin panel: `https://collectorium.onrender.com/admin`
- Health check: `https://collectorium.onrender.com/healthz/`

---

### ADIM 6: SUPERUSER OLUŞTURUN

Render Dashboard'da:

1. **Web Service → Shell** tab'ına gidin
2. Şu komutu çalıştırın:

```bash
python manage.py createsuperuser
```

3. Username, email, password girin
4. **Artık admin paneline girebilirsiniz!** 🎉

---

## 🔧 OPSİYONEL: GOOGLE OAUTH AYARLARI

Eğer Google ile giriş çalıştırmak isterseniz:

### 1. Render Environment Variables

**Dashboard → Environment** tab'ında:

```
GOOGLE_CLIENT_ID = your-google-client-id
GOOGLE_CLIENT_SECRET = your-google-client-secret
```

### 2. Google Cloud Console

**Authorized redirect URIs** kısmına ekleyin:

```
https://collectorium.onrender.com/accounts/google/login/callback/
```

---

## 📊 ÖZELLİKLER

### ✅ Ücretsiz Plan İçeriği:

- **750 saat/ay** web service
- **PostgreSQL database** (90 gün sonra spins down)
- **100 GB bandwidth/ay**
- **Automatic HTTPS/SSL**
- **Auto-deploy** from GitHub
- **Custom domain** (isterseniz)

### 🚀 Performans:

- **Region:** Frankfurt (Türkiye'ye yakın!)
- **Workers:** Gunicorn 4 worker
- **Database:** PostgreSQL 15
- **Static files:** WhiteNoise (ultra-fast)

---

## 🔄 GÜNCELLEMELER

Her kod değişikliğinde:

```powershell
git add .
git commit -m "Your update"
git push
```

**Render otomatik olarak:**
1. Değişikliği algılar
2. Build yapar
3. Deploy eder
4. Zero-downtime restart

**TAK TAK TAK!** 🚀

---

## 📈 MONİTORİNG

### Logs

**Dashboard → Logs** → Real-time log stream

### Metrics

**Dashboard → Metrics** → CPU, Memory, Requests

### Health Check

Otomatik: `https://collectorium.onrender.com/healthz/`

---

## ⚡ HIZLI REFERANS

| Ne yapmak istiyorsunuz? | Nasıl yapılır? |
|-------------------------|----------------|
| **Logs görmek** | Dashboard → Logs |
| **Database erişimi** | Dashboard → Database → Connect |
| **Environment variable eklemek** | Dashboard → Environment |
| **Manuel deploy** | Dashboard → Manual Deploy → Deploy latest commit |
| **Shell erişimi** | Dashboard → Shell |
| **Custom domain** | Dashboard → Settings → Custom Domain |

---

## 🎉 BAŞARILI!

Collectorium artık Render'da canlı! 

**Özellikleri:**
- ✅ Otomatik HTTPS
- ✅ Otomatik deploy
- ✅ PostgreSQL database
- ✅ Static files serving
- ✅ Google OAuth hazır
- ✅ Professional hosting

**Keyifle kullanın!** 🚀🎊

---

## 🆘 SORUN GİDERME

### Deploy Başarısız Olursa

1. **Logs** tab'ını kontrol edin
2. `build.sh` çalıştı mı?
3. Environment variables doğru mu?

### 500 Error Alıyorsanız

1. **Logs** → Django error mesajlarını okuyun
2. `SECRET_KEY` set edilmiş mi?
3. `DATABASE_URL` otomatik eklendi mi?

### Static Files Yüklenmiyor

- `collectstatic` otomatik çalışır (`build.sh`)
- WhiteNoise middleware aktif

---

**Sorularınız için buradayım!** 😊

