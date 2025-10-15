# 🎨 CEO İÇİN GÖRSEL YERLEŞİM DİREKTİFİ

## 📍 Görselleri Nereye Koyacaksınız?

Tüm hero görselleri şu klasöre yerleştirilmelidir:

```
static/images/hero/
```

## 📦 Gerekli Dosyalar ve İsimlendirme

### 1. Arka Plan Görseli
**Dosya Adı:** `hero_background.jpg`  
**Tam Yol:** `static/images/hero/hero_background.jpg`

**Özellikler:**
- **Boyut:** 1920x1080px (Full HD) veya 2560x1440px (2K önerilir)
- **Format:** JPG
- **Maksimum Dosya Boyutu:** 500KB
- **İçerik:** Koleksiyon temalı atmosferik görsel (kartlar, figürler, çizgi romanlar)

### 2. Süzülen Koleksiyon Parçaları (PNG)

| Dosya Adı | Tam Yol | Önerilen İçerik |
|-----------|---------|-----------------|
| `hero_item_1.png` | `static/images/hero/hero_item_1.png` | Pokémon kartı (Charizard vb.) |
| `hero_item_2.png` | `static/images/hero/hero_item_2.png` | Koleksiyonel figür (Funko Pop) |
| `hero_item_3.png` | `static/images/hero/hero_item_3.png` | İkonik çizgi roman kapağı |
| `hero_item_4.png` | `static/images/hero/hero_item_4.png` | Magic: The Gathering kartı |
| `hero_item_5.png` | `static/images/hero/hero_item_5.png` | Nadir koleksiyon parçası |
| `hero_item_6.png` | `static/images/hero/hero_item_6.png` | Özel seri kart/figür |

**Özellikler:**
- **Boyut:** 200-400px genişlik
- **Format:** PNG (ŞEFFthe background - **ÇOK ÖNEMLİ!**)
- **Maksimum Dosya Boyutu:** 100KB/dosya
- **Optimizasyon:** TinyPNG.com kullanın

## 🚀 Adım Adım Kurulum

### Adım 1: Görselleri Hazırlayın

1. Görselleri yukarıdaki özelliklere uygun şekilde hazırlayın
2. PNG dosyaları için arka planı kaldırın (Photoshop, remove.bg vb.)
3. Görselleri optimize edin (TinyPNG, ImageOptim)

### Adım 2: Klasöre Kopyalayın

**Manuel Yöntem:**
1. Windows Explorer'da şu klasörü açın:
   ```
   C:\Users\Eren Nezih\Desktop\Eren Proje ve İşler\Collectorium\static\images\hero\
   ```
2. Hazırladığınız 7 dosyayı bu klasöre kopyalayın

**PowerShell Yöntemi:**
```powershell
# Proje klasörüne git
cd "C:\Users\Eren Nezih\Desktop\Eren Proje ve İşler\Collectorium"

# Görselleri kopyala (görsellerin bulunduğu klasörü değiştirin)
Copy-Item "C:\YourImageFolder\hero_background.jpg" -Destination "static\images\hero\"
Copy-Item "C:\YourImageFolder\hero_item_1.png" -Destination "static\images\hero\"
Copy-Item "C:\YourImageFolder\hero_item_2.png" -Destination "static\images\hero\"
Copy-Item "C:\YourImageFolder\hero_item_3.png" -Destination "static\images\hero\"
Copy-Item "C:\YourImageFolder\hero_item_4.png" -Destination "static\images\hero\"
Copy-Item "C:\YourImageFolder\hero_item_5.png" -Destination "static\images\hero\"
Copy-Item "C:\YourImageFolder\hero_item_6.png" -Destination "static\images\hero\"
```

### Adım 3: Sunucuyu Yeniden Başlatın

```powershell
# Django development server'ı durdur (Ctrl+C)
# Sonra tekrar başlat:
python manage.py runserver
```

### Adım 4: Test Edin

1. Tarayıcıda açın: `http://127.0.0.1:8000/`
2. Ana sayfada hero bölümünü kontrol edin
3. Görmelisiniz:
   - ✅ Arka plan görseli (hafif şeffaf)
   - ✅ 6 adet süzülen koleksiyon parçası
   - ✅ Yavaş ve zarif animasyonlar

## ❌ Sık Karşılaşılan Hatalar

### Hata 1: Görseller Görünmüyor
**Çözüm:**
- Dosya adlarını kontrol edin (küçük/büyük harf duyarlı!)
- Uzantıları kontrol edin (`.jpg` ve `.png` olmalı)
- Hard refresh yapın: `Ctrl + Shift + R`

### Hata 2: PNG Arka Planı Şeffaf Değil
**Çözüm:**
- Görseli Photoshop'ta açın
- Background layer'ı silin
- "Save for Web" ile PNG-24 formatında kaydedin

### Hata 3: Görseller Çok Yavaş Yükleniyor
**Çözüm:**
- TinyPNG.com ile sıkıştırın
- Hero background için max 500KB
- Her PNG için max 100KB

## 🎨 Görsel Önerileri

### Arka Plan İçin
- **İyi örnek:** Ahşap masada dizilmiş koleksiyon kartları, yumuşak ışık
- **Kötü örnek:** Çok karmaşık, parlak renkli, low-res görsel

### Koleksiyon Parçaları İçin
- **İyi örnek:** Net, yüksek çözünürlük, şeffaf arka plan, ikonik ürünler
- **Kötü örnek:** Bulanık, beyaz arka plan, jenerik ürünler

## ✅ Checklist

Görselleri yerleştirmeden önce kontrol edin:

- [ ] Tüm dosya adları doğru (hero_background.jpg, hero_item_1.png vb.)
- [ ] PNG dosyaları şeffaf arka planlı
- [ ] Dosya boyutları optimum (JPG <500KB, PNG <100KB)
- [ ] Görseller yüksek kaliteli ve net
- [ ] Klasör yolu doğru: `static/images/hero/`
- [ ] Toplam 7 dosya var

## 🎯 Son Adım

Görselleri yerleştirdikten sonra:

1. Ana sayfayı açın
2. Ekran görüntüsü alın
3. Memnun kalırsanız → Devam ✅
4. Değişiklik isterseniz → Görselleri değiştirin ve tekrar test edin

---

**Herhangi bir sorunuz varsa, bu raporu referans gösterin!**

