# Search & Discovery Analysis (P0→P1→P2)

## Mevcut Durum
- Veri: `Listing` (price, condition, stock, is_active, created_at), `Product` (category, brand), `Store` (is_verified)
- Filtre/Sıralama: temel filtreler marketplace içinde; kategori/mağaza bazlı listelemeler var

## Kategori Sözlüğü (Örnek)
- Ortak facetler: price_range (min,max), condition (enum), seller_rating (float band), brand (text)
- TCG: set, rarity, grade (text/enums)
- Figur: series, scale (text/enums)

## Sıralama İlkeleri
- Varsayılan: Yeni (created_at desc) veya Alaka (basit: title/product name LIKE)
- Diğer: price asc/desc, seller_rating desc, popularity (views/favorites proxy)

## Performans Bütçesi
- Staging hedefleri: TTFB < 400ms (95p), tek sorgu sayfası < 20; N+1 yok
- İndeks önerileri: Listing(is_active, created_at), Listing(price), Listing(condition), Product(category_id, brand)
- ORM: select_related(product, store), prefetch_related(images)

## Flag & Rollout Planı
- FEATURE_SEARCH_V1, FEATURE_SAVED_SEARCHES, FEATURE_COMPARE, FEATURE_PRICE_HISTORY, FEATURE_MAP_SEARCH
- Kapalı gelir, staging’de aç: kademeli rollout → canary → tam açılış

## A11y/UX İlkeleri
- Klavye ile erişim, aria-label’lar, “filtreyi temizle”, aktif filtreler pill olarak görünür
- Boş sonuç mesajı ve yönlendirici metin

## Gizlilik & KVKK
- Lokasyon (P2) için izinli, yaklaşık gösterim; e-posta uyarılarında frekans kotası

## Riskler & Cut-Scope
- İlk aşamada 4 facet: price, condition, brand, seller_rating
- Gelişmiş kategori facetleri ikinci iterasyonda

## KPI Etkisi (Beklenti)
- Arama→Görüntüleme→Sepet dönüşümünde artış; boş sonuç oranında düşüş

