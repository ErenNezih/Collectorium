# 🛡️ AEGIS OPERASYONU - Google OAuth Kurulum Rehberi

## Collectorium - Google ile Giriş Aktive Etme

Bu rehber, platformunuzda "Google ile Giriş Yap" özelliğini aktive etmek için gerekli tüm adımları içerir.

---

## 📋 ÖN KOŞULLAR

✅ Django projeniz çalışır durumda olmalı  
✅ Superuser (yönetici) hesabınız oluşturulmuş olmalı  
✅ Google hesabınız olmalı

---

## 🚀 ADIM 1: Site Ayarlarını Yapılandırın

Terminal'de şu komutu çalıştırın:

```bash
python manage.py setup_google_oauth
```

Bu komut, gerekli Site nesnesini otomatik olarak oluşturacak veya güncelleyecektir.

---

## 🔑 ADIM 2: Google Cloud Console'da Proje Oluşturun

### 2.1. Google Cloud Console'a Gidin
[https://console.cloud.google.com/](https://console.cloud.google.com/)

### 2.2. Yeni Proje Oluşturun
- Üst menüden "Select a project" > "New Project"
- Proje adı: **Collectorium**
- "Create" butonuna tıklayın

### 2.3. OAuth Consent Screen'i Yapılandırın
1. Sol menüden "APIs & Services" > "OAuth consent screen"
2. User Type: **External** seçin
3. "Create" butonuna tıklayın
4. Formu doldurun:
   - **App name:** Collectorium
   - **User support email:** Sizin e-posta adresiniz
   - **Developer contact information:** Sizin e-posta adresiniz
5. "Save and Continue" ile ilerleyin
6. Scopes ekranını boş bırakıp "Save and Continue"
7. Test users ekranında kendi Gmail adresinizi ekleyin
8. "Save and Continue" ile tamamlayın

### 2.4. OAuth Client ID Oluşturun
1. Sol menüden "Credentials" > "+ CREATE CREDENTIALS" > "OAuth client ID"
2. Application type: **Web application**
3. Name: **Collectorium Web Client**
4. **Authorized redirect URIs** bölümüne ekleyin:
   ```
   http://127.0.0.1:8000/accounts/google/login/callback/
   ```
   
   ⚠️ **ÇOK ÖNEMLİ:** Bu URL'yi TAM olarak bu şekilde girin!

5. "Create" butonuna tıklayın

### 2.5. Anahtarları Kaydedin
- Karşınıza çıkan pencereden:
  - **Client ID** (yaklaşık 70 karakter)
  - **Client Secret** (yaklaşık 35 karakter)
- Bu iki değeri güvenli bir yere kopyalayın!

---

## ⚙️ ADIM 3: Django Admin'e Anahtarları Girin

### 3.1. Admin Paneline Giriş Yapın
Tarayıcınızda: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

### 3.2. Social Application Ekleyin
1. "SOCIAL ACCOUNTS" bölümünde "Social applications" bulun
2. Sağ üstteki "+ Add social application" butonuna tıklayın

### 3.3. Formu Doldurun
- **Provider:** `Google` seçin (dropdown'dan)
- **Name:** `Google OAuth` yazın
- **Client id:** Google'dan aldığınız **Client ID**'yi buraya yapıştırın
- **Secret key:** Google'dan aldığınız **Client Secret**'ı buraya yapıştırın
- **Key:** Boş bırakın
- **Sites:** "Available sites" listesinden siteyi seçip sağ tarafa (Chosen sites) taşıyın
  - `127.0.0.1:8000` veya `Collectorium (Development)` olmalı

### 3.4. Kaydedin
- "SAVE" butonuna tıklayın

---

## ✅ ADIM 4: Test Edin

### 4.1. Çıkış Yapın
Eğer halen giriş yaptıysanız, çıkış yapın.

### 4.2. Giriş Sayfasına Gidin
[http://127.0.0.1:8000/accounts/login/](http://127.0.0.1:8000/accounts/login/)

### 4.3. "Google ile Giriş Yap" Butonuna Tıklayın
- Google hesap seçme ekranı açılacak
- Hesabınızı seçin ve izin verin
- İlk kez giriş yapıyorsanız → **Onboarding sayfasına** yönlendirileceksiniz
- Daha önce giriş yaptıysanız → Doğrudan platformumuza giriş yapacaksınız

---

## 🎯 BAŞARI KRİTERLERİ

✅ "Google ile Giriş Yap" butonu çalışıyor  
✅ Google'a yönlendirme sorunsuz gerçekleşiyor  
✅ Yeni kullanıcılar **özel onboarding sayfasına** yönlendiriliyor  
✅ Eski kullanıcılar doğrudan giriş yapıyor  
✅ Tüm ara sayfalar **Collectorium markasını** taşıyor

---

## 🐛 Sorun Giderme

### "redirect_uri_mismatch" Hatası
**Sebep:** Google Cloud Console'daki redirect URI yanlış yapılandırılmış.

**Çözüm:**
1. Google Cloud Console > Credentials > OAuth 2.0 Client IDs
2. İlgili client'a tıklayın
3. "Authorized redirect URIs" bölümüne tam olarak şunu ekleyin:
   ```
   http://127.0.0.1:8000/accounts/google/login/callback/
   ```
4. Kaydedin ve birkaç dakika bekleyin

### Admin Panelde "Social applications" Görünmüyor
**Çözüm:**
1. Superuser olarak giriş yaptığınızdan emin olun
2. `python manage.py migrate` komutunu çalıştırın
3. Sunucuyu yeniden başlatın: `python manage.py runserver`

### Google'dan Döndükten Sonra Hata Alıyorum
**Çözüm:**
1. Admin panelde Social Application'ın **Sites** kısmının dolu olduğundan emin olun
2. `SITE_ID = 1` ayarının `settings.py`'de olduğunu kontrol edin

---

## 🌐 Canlı Yayına Geçerken (Production)

Canlı siteye geçtiğinizde:

1. Google Cloud Console'da yeni bir redirect URI ekleyin:
   ```
   https://www.collectorium.com.tr/accounts/google/login/callback/
   ```

2. Django Admin'de Site nesnesini güncelleyin:
   - Domain: `www.collectorium.com.tr`
   - Name: `Collectorium`

3. OAuth Consent Screen'i "In production" moduna alın

---

## 📞 Destek

Herhangi bir sorunla karşılaşırsanız:
- Hata mesajlarını tam olarak kaydedin
- Google Cloud Console ayarlarını kontrol edin
- Django Admin'deki Social Application ayarlarını gözden geçirin

---

**'Aegis' Operasyonu başarıyla tamamlandı.**  
**Platform, dünya standartlarında Google OAuth entegrasyonu için hazırdır.** 🛡️
