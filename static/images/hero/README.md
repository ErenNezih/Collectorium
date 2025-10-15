# Hero Görselleri Klasörü

Bu klasör, ana sayfanın hero bölümünde kullanılacak görselleri içerir.

## Gerekli Dosyalar

### 1. Arka Plan Görseli
- **Dosya Adı:** `hero_background.jpg`
- **Önerilen Boyut:** 1920x1080px (Full HD) veya daha yüksek
- **Format:** JPG
- **Açıklama:** Hero bölümünün sinematik arka plan görseli

### 2. Süzülen Koleksiyon Parçaları (PNG - Şeffaf Arka Plan)
- `hero_item_1.png` - Örn: Pokémon kartı
- `hero_item_2.png` - Örn: Figür
- `hero_item_3.png` - Örn: Çizgi roman kapağı
- `hero_item_4.png` - Örn: TCG kartı
- `hero_item_5.png` - Örn: Koleksiyon parçası
- `hero_item_6.png` - Örn: Özel kart

**Önerilen Boyut:** 200-400px genişlik  
**Format:** PNG (şeffaf arka plan)  
**Açıklama:** Hero bölümünde zarif animasyonlarla süzülen ürün görselleri

## Görsel Optimizasyon İpuçları

- Görselleri yüklemeden önce sıkıştırın (TinyPNG, ImageOptim vb.)
- Arka plan görseli için max 500KB hedefleyin
- PNG görselleri için max 100KB/dosya hedefleyin
- Yüksek çözünürlüklü görseller kullanın (Retina display için)

## Kurulum

Görselleri hazırladıktan sonra, bu klasöre yerleştirin ve şu komutu çalıştırın:

```bash
python manage.py collectstatic --noinput
```

Bu komut görselleri production ortamına kopyalayacaktır.
