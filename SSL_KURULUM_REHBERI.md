# 🔒 SSL Sertifikası Kurulum Rehberi
## Collectorium.com.tr - Güvenli ve Kademeli Kurulum

**Önemli:** Bu rehber sitenin bozulmaması için kademeli bir yaklaşım kullanır.

---

## 📋 ÖN HAZIRLIK

### Mevcut Durum Kontrolü
- ✅ Django ayarları SSL için pasif (güvenli)
- ✅ Site HTTP üzerinden çalışıyor
- ⚠️ Domainler AutoSSL'den hariç tutulmuş

---

## 🎯 ADIM 1: AutoSSL'e Domainleri Dahil Et

### 1.1. cPanel'e Giriş
```
cPanel → SSL/TLS → SSL/TLS Status
```

### 1.2. Domainleri Seç
**Aşağıdaki domainler için "+ Include during AutoSSL" linkine tıkla:**
- ✅ `collectorium.com.tr` (ANA DOMAIN - MUTLAKA EKLE)
- ✅ `www.collectorium.com.tr` (WWW SUBDOMAIN - MUTLAKA EKLE)

**Diğer subdomainler için şimdilik ekleme:**
- ⏸️ `mail.collectorium.com.tr` (şimdilik atla)
- ⏸️ `cpanel.collectorium.com.tr` (şimdilik atla)
- ⏸️ Diğer subdomainler (şimdilik atla)

### 1.3. Durum Kontrolü
✅ Başarılı ise:
- Her iki domain için kırmızı "yasak" işareti kalkmalı
- "Certificate Status" → "Included" görünmeli

---

## 🚀 ADIM 2: AutoSSL Çalıştır

### 2.1. AutoSSL'i Başlat
```
cPanel → SSL/TLS Status → "Run AutoSSL" butonuna tıkla
```

### 2.2. Bekleme Süresi
⏱️ **5-15 dakika** bekle (cPanel sertifikayı oluşturur)

### 2.3. Durum Kontrolü
```
cPanel → SSL/TLS Status
```

**Başarılı olursa göreceksin:**
- ✅ `collectorium.com.tr` → "Valid Certificate" (veya benzer)
- ✅ `www.collectorium.com.tr` → "Valid Certificate" (veya benzer)
- ✅ Yeşil kilit ikonu görünmeli

**Hata olursa:**
- ⚠️ DNS propagation sorunu olabilir
- ⚠️ Domain doğru IP'ye yönlenmemiş olabilir
- Çözüm: DNS kontrolü yap (whatsmydns.net)

---

## 🧪 ADIM 3: SSL Testi (Django Ayarları Değişmeden)

### 3.1. Tarayıcıda Test
```
https://collectorium.com.tr
https://www.collectorium.com.tr
```

**Beklenen Sonuç:**
- ✅ Yeşil kilit ikonu görünmeli
- ✅ "Güvenli" yazısı görünmeli
- ✅ Site açılmalı (şimdilik HTTP'ye redirect olabilir, sorun değil)

**Hata varsa:**
- ⚠️ Sertifika henüz aktif olmamış olabilir
- ⏱️ 15-30 dakika daha bekle ve tekrar dene

### 3.2. SSL Checker ile Doğrula
```
https://www.sslshopper.com/ssl-checker.html
```
Domain'i gir ve durumu kontrol et.

---

## ⚙️ ADIM 4: Django Ayarlarını Aktifleştir (KADEMELİ)

### ⚠️ ÖNEMLİ: Bu adımı sadece SSL sertifikası başarıyla kurulduktan sonra yap!

### 4.1. cPanel Environment Variables Güncelle

```
cPanel → Python App → collectorium → Environment Variables
```

**Şu değişkeni ekle/güncelle:**
```
Name: SECURE_SSL_REDIRECT
Value: True
```

### 4.2. Django Settings Güncelle

`collectorium/settings/hosting.py` dosyasını güncelle:

```python
# Cookies - SSL aktifken True olmalı
SESSION_COOKIE_SECURE = True  # False'dan True'ya değiştir
CSRF_COOKIE_SECURE = True     # False'dan True'ya değiştir
```

### 4.3. Git Push ve Deploy

```bash
git add collectorium/settings/hosting.py
git commit -m "feat: Enable SSL security settings after certificate installation"
git push origin main
```

### 4.4. Sunucuda Restart

```bash
# cPanel Terminal'de:
cd /home/collecto/collectorium
touch tmp/restart.txt
```

---

## ✅ ADIM 5: Final Test

### 5.1. HTTP → HTTPS Redirect Testi
```
http://collectorium.com.tr
```
**Beklenen:** Otomatik olarak `https://collectorium.com.tr`'ye yönlendirmeli

### 5.2. HTTPS Çalışma Testi
```
https://collectorium.com.tr
```
**Beklenen:**
- ✅ Yeşil kilit ikonu
- ✅ Site normal çalışmalı
- ✅ Formlar çalışmalı (login, signup, vb.)

### 5.3. Mixed Content Kontrolü
- Browser Console'u aç (F12)
- "Mixed Content" uyarısı olmamalı
- Tüm kaynaklar HTTPS üzerinden yüklenmeli

---

## 🚨 SORUN GİDERME

### Sorun 1: AutoSSL Başarısız
**Çözüm:**
1. DNS kontrolü yap: `whatsmydns.net`
2. Domain doğru IP'ye yönlenmeli (`45.151.250.159`)
3. 24 saat bekle ve tekrar dene

### Sorun 2: SSL Aktif Ama Site Bozuldu
**Acil Çözüm:**
```bash
# cPanel → Python App → Environment Variables
SECURE_SSL_REDIRECT=False
```
Sonra restart: `touch tmp/restart.txt`

### Sorun 3: Mixed Content Uyarıları
**Çözüm:**
- Tüm template'lerde `http://` yerine `https://` kullan
- Ya da `//` kullan (protocol-relative URL)

---

## 📊 BAŞARI KRİTERLERİ

✅ SSL sertifikası aktif ve geçerli
✅ HTTPS bağlantısı çalışıyor
✅ HTTP → HTTPS redirect çalışıyor
✅ Site normal çalışıyor (bozulma yok)
✅ Browser'da yeşil kilit ikonu görünüyor
✅ Mixed content uyarısı yok

---

## 📝 NOTLAR

- **Sitenin bozulmaması için:** Adım 4'ü sadece SSL sertifikası başarıyla kurulduktan sonra yapın
- **Test süresi:** Her adımda 5-15 dakika bekleyin
- **Yedek:** Bu rehberi takip ederseniz site bozulmaz, sadece SSL aktif olur

---

**Son Güncelleme:** 2025-01-20
**Durum:** Güvenli kurulum rehberi hazır ✅

