# 🔒 cPanel Force HTTPS Redirect Aktifleştirme
## Collectorium.com.tr - Son Adım

**Sorun:** Tarayıcı "Güvenli değil" gösteriyor çünkü cPanel'de Force HTTPS Redirect aktif değil.

---

## ✅ ÇÖZÜM: cPanel'de Force HTTPS Redirect Aktifleştir

### Adım 1: cPanel SSL/TLS Bölümüne Git
```
cPanel → SSL/TLS → Force HTTPS Redirect
```

### Adım 2: Force HTTPS Redirect'i Aktifleştir
1. **"Force HTTPS Redirect"** butonuna tıkla
2. Açılan sayfada:
   - Domain seç: `collectorium.com.tr`
   - **"Force HTTPS Redirect"** checkbox'ını işaretle
   - **"Save"** butonuna tıkla

### Adım 3: www Subdomain için de Aktifleştir
Aynı işlemi `www.collectorium.com.tr` için de yap:
1. Domain seç: `www.collectorium.com.tr`
2. **"Force HTTPS Redirect"** checkbox'ını işaretle
3. **"Save"** butonuna tıkla

---

## ✅ Adım 4: Test Et

### Tarayıcı Cache'ini Temizle
**Chrome:**
```
Ctrl + Shift + Delete → "Cached images and files" seç → Temizle
```

**Veya:**
```
Ctrl + F5 (Hard refresh)
```

### Test Adımları:
1. **HTTP → HTTPS Redirect Testi:**
   ```
   http://collectorium.com.tr
   ```
   **Beklenen:** Otomatik olarak `https://collectorium.com.tr`'ye yönlendirmeli

2. **HTTPS Testi:**
   ```
   https://collectorium.com.tr
   ```
   **Beklenen:**
   - ✅ Yeşil kilit ikonu görünmeli
   - ✅ "Güvenli" yazısı görünmeli
   - ✅ "Güvenli değil" uyarısı KALKMALI

---

## 🎯 BEKLENEN SONUÇLAR

Force HTTPS Redirect aktif olduktan sonra:
- ✅ HTTP istekleri otomatik HTTPS'e yönlendirilir (Apache seviyesinde)
- ✅ Tarayıcı yeşil kilit ikonu gösterir
- ✅ "Güvenli" yazısı görünür
- ✅ "Güvenli değil" uyarısı kalkar
- ✅ SEO için de iyi (Google HTTPS'i tercih eder)

---

## 🚨 SORUN GİDERME

### Sorun 1: Force HTTPS Redirect Butonu Görünmüyor
**Çözüm:**
- cPanel → SSL/TLS → SSL/TLS Status
- Domain için sertifika aktif olmalı
- Eğer sertifika aktif değilse, önce sertifikayı kur

### Sorun 2: Redirect Çalışmıyor
**Kontrol:**
```bash
# cPanel Terminal'de:
curl -I http://collectorium.com.tr
```
**Beklenen:** `301 Moved Permanently` ve `Location: https://collectorium.com.tr`

**Çözüm:**
- Force HTTPS Redirect'i tekrar aktifleştir
- 5-10 dakika bekle (Apache restart gerekebilir)
- Tekrar test et

### Sorun 3: Hala "Güvenli değil" Gösteriyor
**Kontrol Listesi:**
1. ✅ SSL sertifikası aktif mi? (cPanel → SSL/TLS Status)
2. ✅ Force HTTPS Redirect aktif mi? (cPanel → SSL/TLS → Force HTTPS Redirect)
3. ✅ Tarayıcı cache'i temizlendi mi? (Ctrl + Shift + Delete)
4. ✅ Hard refresh yapıldı mı? (Ctrl + F5)
5. ✅ Farklı tarayıcıda test edildi mi? (Chrome, Firefox, Edge)

---

## 📊 BAŞARI KRİTERLERİ

✅ Force HTTPS Redirect aktif
✅ HTTP → HTTPS redirect çalışıyor
✅ Tarayıcı yeşil kilit ikonu gösteriyor
✅ "Güvenli" yazısı görünüyor
✅ "Güvenli değil" uyarısı kalktı
✅ Site normal çalışıyor

---

**Son Güncelleme:** 2025-01-20
**Durum:** Force HTTPS Redirect aktifleştirme rehberi hazır ✅

