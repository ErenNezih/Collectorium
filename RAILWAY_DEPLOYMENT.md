# 🚀 COLLECTORIUM - RAILWAY DEPLOYMENT GUIDE

**2 dakikada deploy! GitHub'a push → Otomatik canlı!**

---

## 📋 GEREKLİLER

- ✅ GitHub hesabı
- ✅ Railway.app hesabı (GitHub ile giriş yapın)
- ✅ Collectorium projeniz

---

## 🎯 ADIM 1: GITHUB'A PUSH EDIN

Eğer projeniz henüz GitHub'da değilse:

```bash
cd "C:\Users\Eren Nezih\Desktop\Eren Proje ve İşler\Collectorium"

# Git initialize
git init
git add .
git commit -m "Initial commit for Railway deployment"

# GitHub'da yeni repo oluşturun (github.com/new)
# Sonra:
git branch -M main
git remote add origin https://github.com/YOURUSERNAME/Collectorium.git
git push -u origin main
```

---

## 🚂 ADIM 2: RAILWAY'E DEPLOY

### 1. Railway'e Giriş Yapın

🔗 https://railway.app/

**"Login with GitHub"** → 1 saniye hesap açıldı!

### 2. New Project

- **"New Project"** butonuna tıklayın
- **"Deploy from GitHub repo"** seçin
- **Collectorium** reponuzu seçin

### 3. Otomatik Deploy Başlıyor!

Railway otomatik olarak:
- ✅ Projenizi detect eder
- ✅ Python 3.11 kurar
- ✅ Dependencies yükler
- ✅ PostgreSQL database oluşturur
- ✅ Static files toplar
- ✅ Migration çalıştırır
- ✅ Deploy eder!

⏱️ **Bekleme:** 2-3 dakika

---

## 🔧 ADIM 3: ENVIRONMENT VARIABLES AYARLA

Deploy bittikten sonra:

1. **"Variables"** tab'ına gidin
2. Şu değişkenleri ekleyin:

### Gerekli Variables:

```bash
DJANGO_SETTINGS_MODULE=collectorium.settings.railway
SECRET_KEY=your-secret-key-here  # Güçlü bir key oluşturun
DEBUG=False
ALLOWED_HOSTS=*.up.railway.app
```

### SECRET_KEY Oluşturma:

Lokal terminalinizde:

```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

Çıkan değeri kopyalayıp `SECRET_KEY` variable'ına yapıştırın.

### Opsiyonel Variables:

```bash
# Google OAuth (eğer kullanıyorsanız)
GOOGLE_CLIENT_ID=your-client-id
GOOGLE_CLIENT_SECRET=your-client-secret

# Email (opsiyonel)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

---

## 🗄️ ADIM 4: DATABASE ZATEN HAZIR!

Railway otomatik olarak **PostgreSQL database** oluşturmuştur.

`DATABASE_URL` environment variable otomatik set edilmiştir.

**Hiçbir şey yapmanıza gerek yok!** ✅

---

## 👤 ADIM 5: SUPERUSER OLUŞTUR

Railway dashboard'da:

1. **"Deployments"** tab → En son deployment'a tıklayın
2. **"View Logs"** → Log ekranı açılacak
3. Sağ üstteki **"⋮"** (3 nokta) → **"Run a command"**
4. Şu komutu çalıştırın:

```bash
python manage.py createsuperuser
```

Username, email, password girin.

---

## 🎉 ADIM 6: SİTENİZ CANLIDA!

Railway size otomatik bir URL vermiştir:

**Settings** tab → **Domains** bölümünde göreceksiniz:

```
https://collectorium-production.up.railway.app
```

veya

```
https://collectorium-production-xxxx.up.railway.app
```

### Test Edin:

🌐 **Ana Sayfa:**
```
https://your-app.up.railway.app
```

🔐 **Admin:**
```
https://your-app.up.railway.app/admin
```

---

## 🔄 GÜNCELLEME (OTOMATIK!)

Railway **GitHub'a her push'ta otomatik deploy** eder!

```bash
# Lokal'de değişiklik yapın
git add .
git commit -m "Feature: yeni özellik"
git push

# Railway otomatik olarak detect eder ve deploy eder!
# 2-3 dakika içinde canlı olur!
```

**Hiçbir şey yapmanıza gerek yok!** Railway her push'u izler ve deploy eder! 🎉

---

## 🌐 CUSTOM DOMAIN (Opsiyonel)

Kendi domaininizi bağlamak için:

1. Railway → **Settings** → **Domains**
2. **"Custom Domain"** → Domain adınızı girin
3. Railway size DNS kayıtlarını verecek
4. Domain sağlayıcınızda (GoDaddy, Namecheap vb.) DNS kayıtlarını ekleyin
5. ✅ **Bitti!**

---

## 📊 ÜCRETSİZ PLAN LİMİTLERİ

Railway Free Plan:
- ✅ **500 saat/ay** (günde ~16 saat)
- ✅ **Unlimited disk**
- ✅ **PostgreSQL database** dahil
- ✅ **Custom domain** bağlanabilir
- ✅ **HTTPS** otomatik

**Collectorium için fazlasıyla yeterli!** 🎯

---

## 🆘 SORUN GİDERME

### "Build Failed"

**Deployments** → Logs kontrol edin

**Sık hatalar:**
- `requirements.txt` eksik/yanlış
- Django settings hatası
- Migration hatası

### Static Files Yüklenmiyor

`railway.json` dosyasının doğru olduğundan emin olun.

### Database Connection Error

`DATABASE_URL` variable'ı otomatik set edilmiş olmalı. Variables tab'dan kontrol edin.

---

## ✅ DEPLOYMENT CHECKLIST

- [ ] GitHub'a push yaptım
- [ ] Railway'de project oluşturdum
- [ ] Environment variables ayarladım
- [ ] Deploy tamamlandı
- [ ] Superuser oluşturdum
- [ ] Siteyi test ettim
- [ ] Admin panele giriş yaptım

---

## 🎊 TEBRIKLER!

Collectorium artık **Railway'de canlı**!

🌐 **Site:** https://your-app.up.railway.app  
🔐 **Admin:** https://your-app.up.railway.app/admin  
🚀 **Auto-deploy:** Her GitHub push otomatik yayınlanır!

**15 dakikada production-ready platform!** 🎉

---

## 📞 İLETİŞİM

Sorun yaşarsanız:
- Railway Discord
- Railway Docs: docs.railway.app
- GitHub Issues

**Başarılar!** 🚂✨

