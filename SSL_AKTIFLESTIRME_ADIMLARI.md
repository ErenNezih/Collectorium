# 🔒 SSL Aktifleştirme Adımları
## Collectorium.com.tr - SSL Sertifikası Başarıyla Kuruldu ✅

**Durum:** SSL sertifikası başarıyla kuruldu ve geçerli (29 Ocak 2026'ya kadar)

---

## ✅ ADIM 1: cPanel Environment Variable Ekleme

### 1.1. cPanel'e Giriş
```
cPanel → Python App → collectorium
```

### 1.2. Environment Variables Bölümüne Git
"Environment Variables" veya "App Environment Variables" bölümünü bul

### 1.3. Yeni Variable Ekle
```
Name: SECURE_SSL_REDIRECT
Value: True
```

**Önemli:** Büyük/küçük harf duyarlı değil, ama `True` yazmak daha iyi.

---

## ✅ ADIM 2: Uygulamayı Restart Et

### Seçenek 1: cPanel Terminal'den
```bash
cd /home/collecto/collectorium
touch tmp/restart.txt
```

### Seçenek 2: cPanel Python App'ten
cPanel → Python App → collectorium → "Restart" butonuna tıkla

---

## ✅ ADIM 3: Test Et

### 3.1. HTTP → HTTPS Redirect Testi
```
http://collectorium.com.tr
```
**Beklenen:** Otomatik olarak `https://collectorium.com.tr`'ye yönlendirmeli

### 3.2. HTTPS Çalışma Testi
```
https://collectorium.com.tr
https://www.collectorium.com.tr
```
**Beklenen:**
- ✅ Yeşil kilit ikonu görünmeli
- ✅ "Güvenli" yazısı görünmeli
- ✅ Site normal çalışmalı
- ✅ Formlar çalışmalı (login, signup, vb.)

### 3.3. Browser Console Kontrolü
- F12 tuşuna bas
- Console sekmesine git
- "Mixed Content" uyarısı olmamalı
- Tüm kaynaklar HTTPS üzerinden yüklenmeli

---

## 🎯 BEKLENEN SONUÇLAR

### SSL Aktif Olduktan Sonra:
1. ✅ HTTP → HTTPS otomatik redirect
2. ✅ Yeşil kilit ikonu
3. ✅ Güvenli cookie'ler (SESSION_COOKIE_SECURE=True)
4. ✅ CSRF cookie'leri güvenli (CSRF_COOKIE_SECURE=True)
5. ✅ HSTS headers aktif
6. ✅ Mixed content uyarısı yok

### Django Otomatik Olarak Yapacak:
- `SESSION_COOKIE_SECURE = True` (otomatik)
- `CSRF_COOKIE_SECURE = True` (otomatik)
- `SECURE_HSTS_SECONDS = 31536000` (1 yıl)
- `SECURE_HSTS_INCLUDE_SUBDOMAINS = True`
- `SECURE_HSTS_PRELOAD = True`

---

## 🚨 SORUN GİDERME

### Sorun 1: Redirect Çalışmıyor
**Kontrol:**
```bash
# cPanel Terminal'de:
cd /home/collecto/collectorium
source /home/collecto/virtualenv/collectorium/3.11/bin/activate
python manage.py check --deploy
```

**Çözüm:**
- Environment variable'ın doğru eklendiğinden emin ol (`SECURE_SSL_REDIRECT=True`)
- Uygulamayı restart et

### Sorun 2: Site Bozuldu / 500 Hatası
**Acil Çözüm:**
```
cPanel → Python App → Environment Variables
SECURE_SSL_REDIRECT=False yap
Restart et
```

Sonra tekrar kontrol et ve SSL sertifikasının gerçekten aktif olduğundan emin ol.

### Sorun 3: Mixed Content Uyarıları
**Kontrol:**
- Browser Console'da (F12) "Mixed Content" uyarıları var mı?
- Template'lerde `http://` yerine `https://` kullanıldığından emin ol

---

## 📊 BAŞARI KRİTERLERİ

✅ SSL sertifikası aktif ve geçerli (zaten ✅)
✅ HTTPS bağlantısı çalışıyor
✅ HTTP → HTTPS redirect çalışıyor
✅ Site normal çalışıyor (bozulma yok)
✅ Browser'da yeşil kilit ikonu görünüyor
✅ Mixed content uyarısı yok
✅ Cookie'ler güvenli
✅ HSTS headers aktif

---

**Son Güncelleme:** 2025-01-20
**Durum:** SSL sertifikası kuruldu, Django ayarlarını aktifleştirme zamanı ✅

