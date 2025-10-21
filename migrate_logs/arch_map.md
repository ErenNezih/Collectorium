# 🏗️ COLLECTORIUM - MİMARİ HARİTA

**Tarih**: 20 Ekim 2025  
**Proje**: Collectorium Django 5.2.1  
**Analiz**: Tam Kod İnceleme

---

## 📊 GENEL BAKIŞ

**Toplam Modül**: 14 Django App  
**Toplam Model**: 32+ Model  
**Mimari Tarz**: Monolithic Django (Monorepo)  
**Auth Sistemi**: Custom User + Google OAuth (django-allauth)  
**Sepet**: Session-based (DB-less cart)

---

## 🗺️ MODÜL HARİTASI

### 1. **core** (Temel Uygulama)
**Konum**: `core/`

**Modeller**: Yok (no models.py içerik)

**URL'ler**:
- `/` → home view
- `/marketplace/` → marketplace (listing grid)
- `/listing/<int:listing_id>/` → listing detail
- `/healthz/` → health check (200 OK + JSON)
- `/health/readiness/` → readiness probe
- `/health/liveness/` → liveness probe
- `/hakkimizda/`, `/gizlilik-politikasi/`, `/kullanim-kosullari/`, `/iletisim/`, `/satici-rehberi/`, `/trust/` → Statik sayfalar

**Views**:
- home, marketplace, listing_detail
- AboutView, PrivacyPolicyView, TermsOfServiceView, ContactView, SellerGuideView, TrustCenterView
- handler404, handler500, handler403 (custom error handlers)

**Sorumluluk**: Ana sayfa, marketplace grid, health endpoints, statik sayfalar

**Bağımlılıklar**:
- `listings` → Listing listesi için
- `cart` → Context processor ile sepet görünümü

---

### 2. **accounts** (Kullanıcı Yönetimi)
**Konum**: `accounts/`

**Modeller**:
- **User** (AbstractUser)
  - Fields: role (buyer/seller/admin), store_name, avatar, phone, birth_date
  - Relationships: -
  - Property: full_name

- **Address**
  - Fields: user (FK), address_title, country, city, district, full_address, postal_code, is_default
  - Relationships: User → Address (1:N)
  - Logic: Save metodu ile sadece bir default adres garantisi

- **VerifiedSeller**
  - Fields: user (O2O), company_name, tax_no, status (pending/approved/rejected), reason, verified_at
  - Relationships: User → VerifiedSeller (1:1)
  - Methods: approve(), reject()

- **VerifiedSellerDocument**
  - Fields: verified_seller (FK), file, uploaded_at
  - Relationships: VerifiedSeller → VerifiedSellerDocument (1:N)

**URL'ler**:
- `/account/profile/` → profile view
- `/account/profile/edit/` → profile edit
- `/account/profile/change-password/` → password change
- `/account/orders/` → my orders
- `/account/reviews/` → my reviews
- `/account/favorites/` → my favorites
- `/account/my-listings/` → seller listings
- `/account/user/<username>/` → public profile
- `/account/google/signup/complete/` → Google OAuth onboarding
- `/account/seller/verify/apply/` → verified seller apply
- `/account/seller/verify/status/` → verification status

**Sorumluluk**: Kullanıcı profili, adresler, Google OAuth onboarding, KYC/verified seller

**Bağımlılıklar**:
- `allauth` → Google OAuth entegrasyonu
- `stores` → Seller role ile store ilişkisi
- `listings` → Favorites

---

### 3. **stores** (Mağaza Yönetimi)
**Konum**: `stores/`

**Modeller**:
- **Store**
  - Fields: owner (FK User), name, slug, bio, logo, is_verified, rating_avg, rating_count
  - Relationships: User → Store (1:N)
  - Ordering: -created_at

- **StorePolicy**
  - Fields: store (O2O), return_policy_text, shipping_policy_text, contact_hours, handling_time_days, extra_notes
  - Relationships: Store → StorePolicy (1:1)

**URL'ler**:
- `/stores/` → stores list
- `/stores/<slug:slug>/` → store detail
- `/stores/create/` → create store (seller)
- `/stores/<slug:slug>/edit/` → edit store

**Sorumluluk**: Mağaza yönetimi, mağaza politikaları

**Bağımlılıklar**:
- `accounts` → Store owner User ilişkisi
- `listings` → Store listings

---

### 4. **listings** (İlan Yönetimi)
**Konum**: `listings/`

**Modeller**:
- **Listing**
  - Fields: store (FK), product (FK), title, description, price, currency, condition, stock, is_active, attributes (JSON), city, district
  - Relationships: Store → Listing (1:N), Product → Listing (1:N)
  - Methods: get_primary_image()
  - Ordering: -created_at

- **ListingImage**
  - Fields: listing (FK), image, alt_text, is_primary
  - Relationships: Listing → ListingImage (1:N)
  - Ordering: -is_primary, created_at

- **Favorite**
  - Fields: user (FK), listing (FK)
  - Relationships: User → Favorite (1:N), Listing → Favorite (1:N)
  - Constraints: unique_together=['user', 'listing']

**URL'ler**:
- `/listings/` → listing list
- `/listings/create/` → create listing
- `/listings/<int:pk>/` → listing detail
- `/listings/<int:pk>/edit/` → edit listing
- `/listings/<int:pk>/delete/` → delete listing
- `/listings/<int:pk>/favorite/` → toggle favorite

**Sorumluluk**: İlan CRUD, resimler, favoriler

**Bağımlılıklar**:
- `stores` → Listing store ilişkisi
- `catalog` → Product ilişkisi
- `accounts` → Favorites user ilişkisi

---

### 5. **catalog** (Ürün Kataloğu)
**Konum**: `catalog/`

**Modeller**:
- **Category**
  - Fields: name, slug, parent (FK self), description, image
  - Relationships: Category → Category (hierarchical)
  - Ordering: name

- **Product**
  - Fields: name, slug, category (FK), brand, description
  - Relationships: Category → Product (1:N)
  - Constraints: unique_together=['name', 'brand']
  - Ordering: -created_at

**URL'ler**:
- `/categories/` → categories list
- `/categories/<slug:slug>/` → category detail (with products)

**Sorumluluk**: Kategori hiyerarşisi, ürün tanımları

**Bağımlılıklar**:
- `listings` → Product listings

---

### 6. **cart** (Sepet)
**Konum**: `cart/`

**Modeller**: Yok (Session-based)

**Class**: Cart (session-based cart manager)
- Methods: add(), remove(), save(), clear(), get_total_price()
- Storage: Django session (CART_SESSION_ID key)
- __iter__: Listing objelerini fetch edip yield eder

**URL'ler**:
- `/cart/` → cart view
- `/cart/add/<int:listing_id>/` → add to cart
- `/cart/remove/<int:listing_id>/` → remove from cart
- `/cart/clear/` → clear cart

**Sorumluluk**: Session-based alışveriş sepeti

**Bağımlılıklar**:
- `listings` → Listing objeleri fetch
- Context processor → Template'lerde cart objesi

---

### 7. **orders** (Sipariş Yönetimi)
**Konum**: `orders/`

**Modeller**:
- **Order**
  - Fields: buyer (FK User), total, currency, status (pending/paid/shipped/delivered/cancelled/refunded), shipping_address, notes
  - Relationships: User → Order (1:N)
  - Ordering: -created_at

- **OrderItem**
  - Fields: order (FK), listing (FK), quantity, price_snapshot
  - Relationships: Order → OrderItem (1:N), Listing → OrderItem (1:N)
  - Note: price_snapshot → fiyat değişikliğinden etkilenmesin

**URL'ler**:
- `/orders/` → order list
- `/orders/<int:pk>/` → order detail
- `/orders/checkout/` → checkout process
- `/orders/<int:pk>/confirm/` → confirm order

**Sorumluluk**: Sipariş oluşturma, checkout akışı, price snapshot

**Bağımlılıklar**:
- `accounts` → Buyer user, Address
- `listings` → OrderItem listing ilişkisi
- `cart` → Checkout'ta cart clear
- `payments` → Payment ilişkisi

---

### 8. **reviews** (İlan Yorumları)
**Konum**: `reviews/`

**Modeller**:
- **Review**
  - Fields: user (FK), listing (FK), rating (1-5), comment
  - Relationships: User → Review (1:N), Listing → Review (1:N)
  - Constraints: unique_together=['user', 'listing']
  - Ordering: -created_at

**URL'ler**: Yok (reviews app-level URLs tanımlı değil, muhtemelen listing detail'de inline)

**Sorumluluk**: İlan değerlendirme sistemi

**Bağımlılıklar**:
- `accounts` → User
- `listings` → Listing

---

### 9. **messaging** (Mesajlaşma)
**Konum**: `messaging/`

**Modeller**:
- **Thread**
  - Fields: listing (FK), seller (FK User), buyer (FK User), is_open, last_message_at
  - Relationships: Listing → Thread (1:N), User → Thread (seller/buyer)
  - Constraints: UniqueConstraint per listing-buyer-seller (is_open=True)
  - Ordering: -last_message_at, -created_at

- **ThreadMessage**
  - Fields: thread (FK), sender (FK User), raw_text, redacted_text, has_contact_violation, was_rate_limited, is_reported, read_by_buyer, read_by_seller
  - Relationships: Thread → ThreadMessage (1:N)
  - Ordering: created_at

- **Block**
  - Fields: blocker (FK User), blocked (FK User), reason, expires_at
  - Relationships: User → Block (blocker/blocked)
  - Index: blocker, blocked

**URL'ler**:
- `/m/` → threads list
- `/m/<int:thread_id>/` → thread detail (messages)
- `/m/listing/<int:listing_id>/start/` → start thread for listing

**Sorumluluk**: Buyer-seller mesajlaşma, contact guard (redaction), rate limiting, block mekanizması

**Bağımlılıklar**:
- `accounts` → User (buyer/seller)
- `listings` → Listing (thread konusu)
- `contact_guard.py` → Email/telefon redaksiyon

---

### 10. **search** (Arama & Kaydedilmiş Aramalar)
**Konum**: `search/`

**Modeller**:
- **SavedSearch**
  - Fields: user (FK), name, querystring, frequency (daily/weekly), active, last_run_at, qhash
  - Relationships: User → SavedSearch (1:N)
  - Constraints: unique_together=['user', 'name']
  - Indexes: user, active, frequency

- **PricePoint**
  - Fields: listing (FK), kind (list/sale), price, currency, at, source
  - Relationships: Listing → PricePoint (1:N)
  - Indexes: listing+at, listing+kind+at
  - Purpose: Fiyat geçmişi tracking

**URL'ler**:
- `/search/` → search view
- `/search/saved/` → saved searches
- `/search/saved/create/` → create saved search
- `/search/saved/<int:pk>/delete/` → delete saved search

**Sorumluluk**: Arama fonksiyonalitesi, kaydedilmiş aramalar, fiyat takibi

**Bağımlılıklar**:
- `accounts` → User
- `listings` → Price points

---

### 11. **moderation** (Moderasyon & Risk)
**Konum**: `moderation/`

**Modeller**:
- **Report**
  - Fields: reporter (FK User), target_type (listing/message/user), target_id, reason, description, status (open/actioned/closed)
  - Relationships: User → Report (1:N)
  - Indexes: target_type, target_id, status

- **ModerationAction**
  - Fields: report (FK), action (hide_listing/delete_message/warn_user/ban_user/no_action), severity (low/medium/high), notes, actor (FK User)
  - Relationships: Report → ModerationAction (1:N)

- **RiskSignal**
  - Fields: entity_type, entity_id, type (velocity/high_amount/first_order/contact_leak), severity, meta (JSON)
  - Indexes: entity_type+entity_id+type, created_at
  - Purpose: Risk skorlama için sinyaller

- **Ban**
  - Fields: user (FK), scope (messaging/purchase/sitewide), reason, expires_at, active, created_by (FK User)
  - Relationships: User → Ban (1:N)
  - Indexes: user+scope+active

**URL'ler**:
- `/mod/` → moderation dashboard
- `/mod/reports/` → reports list
- `/mod/reports/<int:pk>/` → report detail
- `/mod/reports/<int:pk>/action/` → take action

**Sorumluluk**: Şikayet yönetimi, moderasyon aksiyonları, ban sistemi, risk sinyalleri

**Bağımlılıklar**:
- `accounts` → User (reporter, actor, banned user)
- `listings`, `messaging` → Reportable entities

---

### 12. **payments** (Ödeme Sistemi)
**Konum**: `payments/`

**Modeller**:
- **Payment**
  - Fields: order (O2O), provider, payment_id, status (initiated/authorized/captured/refunded/failed), amount, currency, three_ds_required, three_ds_status, raw_payload (JSON)
  - Relationships: Order → Payment (1:1)
  - Methods: mark_authorized(), mark_captured(), mark_refunded()
  - Indexes: provider+status, created_at

- **PaymentTransaction**
  - Fields: payment (FK), type (auth/capture/refund/void/fail), amount, idempotency_key, ext_ref, status, raw (JSON)
  - Relationships: Payment → PaymentTransaction (1:N)
  - Constraints: unique idempotency_key
  - Indexes: payment+type, status

- **WebhookEvent**
  - Fields: provider, event_type, signature, payload (JSON), dedupe_key, processed_at, result (ok/err/skipped)
  - Constraints: unique dedupe_key
  - Indexes: provider+event_type, created_at

- **LedgerEntry**
  - Fields: entity (platform/seller), seller (FK Store), order (FK), amount, fee, commission, direction (dr/cr), currency, memo
  - Relationships: Order → LedgerEntry (1:N), Store → LedgerEntry (1:N)
  - Purpose: Double-entry accounting
  - Indexes: order+entity, created_at

- **RefundRequest**
  - Fields: order (FK), type (full/partial), reason, evidence_urls (JSON), status (open/approved/denied), decided_by (FK User), decided_at
  - Relationships: Order → RefundRequest (1:N)
  - Methods: approve(), deny()
  - Indexes: order+status, created_at

**URL'ler**:
- `/payments/` → payment processing
- `/payments/<int:order_id>/process/` → process payment
- `/payments/webhook/` → webhook handler

**Sorumluluk**: Ödeme lifecycle, 3DS, webhook handling, ledger accounting, refund yönetimi

**Bağımlılıklar**:
- `orders` → Order payment ilişkisi
- `stores` → Ledger seller ilişkisi
- `accounts` → Refund decision maker

---

### 13. **shipping** (Kargo)
**Konum**: `shipping/`

**Modeller**: Yok (models.py empty)

**Durum**: P1/P2 kapsamında geliştirilmesi planlanıyor

**Sorumluluk**: Kargo entegrasyonu (gelecek)

---

### 14. **dashboards** (Dashboard)
**Konum**: `dashboards/`

**Modeller**: Yok (models.py'de model tanımı yok)

**Sorumluluk**: Seller/buyer dashboard views (muhtemelen view-only app)

**Bağımlılıklar**: Diğer tüm modüller (data aggregation)

---

## 🔗 VERİ AKIŞI SENARYOLARI

### Senaryo 1: Yeni Kullanıcı Kaydı (Google OAuth)

```
1. User → Google OAuth via allauth
2. CustomSocialAccountAdapter.pre_social_login → Session'a Google data yaz
3. Redirect → /account/google/signup/complete/
4. google_onboarding_complete view:
   - User oluştur (role seçimi, address girişi)
   - Address kaydet
   - SocialAccount link et
   - Eğer seller ise → Store oluştur (signal veya form)
5. Login → redirect /
```

**İlgili Modüller**: accounts, stores, allauth

---

### Senaryo 2: İlan Oluşturma (Seller)

```
1. Seller → /listings/create/
2. Form: Product seç (catalog), fiyat, açıklama, stok, condition, resimler
3. Save:
   - Listing oluştur (store=seller.store)
   - ListingImage kaydet (multiple)
   - Primary image set
4. İlan aktif → Marketplace'de görünür
```

**İlgili Modüller**: listings, stores, catalog

---

### Senaryo 3: Satın Alma Akışı

```
1. Buyer → Listing detail → "Sepete Ekle"
2. Cart.add(listing) → Session'a yaz
3. Buyer → /cart/ → "Checkout"
4. Checkout:
   - Address seçimi (accounts.Address)
   - Cart → Order + OrderItem oluştur (price_snapshot)
   - Cart.clear()
5. Payment:
   - Payment oluştur (provider, status=initiated)
   - 3DS redirect (if required)
   - Webhook → Payment.mark_authorized() → mark_captured()
   - LedgerEntry oluştur (platform+seller)
6. Order.status = 'paid'
7. Seller → Order detail → "Kargoya Ver" → status='shipped'
8. Buyer → Review bırak (reviews.Review)
```

**İlgili Modüller**: cart, orders, payments, accounts, listings, reviews

---

### Senaryo 4: Mesajlaşma

```
1. Buyer → Listing detail → "Satıcıya Sor"
2. Thread oluştur (listing, buyer, seller) OR fetch existing
3. ThreadMessage oluştur (sender=buyer, raw_text)
4. contact_guard check → redacted_text (email/telefon maskele)
5. Seller → Thread'e cevap → ThreadMessage (sender=seller)
6. Block mekanizması: Buyer/Seller birbirini blokayabilir
```

**İlgili Modüller**: messaging, listings, accounts

---

### Senaryo 5: Moderasyon

```
1. User → "Report" butonuna tıkla (listing/message/user)
2. Report oluştur (target_type, target_id, reason)
3. Admin/Moderator → /mod/reports/ → Report detail
4. ModerationAction oluştur (action=hide_listing, severity=high)
5. Listing.is_active = False (eğer hide_listing ise)
6. RiskSignal oluştur (entity_type=listing, type=contact_leak)
7. Eğer ciddi → Ban oluştur (user, scope=sitewide)
```

**İlgili Modüller**: moderation, listings, messaging, accounts

---

## 📐 ÖZEL PATTERN'LER

### 1. **Hierarchical Categories**
- Category → parent (self FK) ile ağaç yapısı
- Recursive query ile sub-categories fetch

### 2. **Price Snapshot Pattern**
- OrderItem.price_snapshot → Listing.price değişse bile sipariş fiyatı korunur

### 3. **Session-Based Cart**
- DB'ye kaydetmeden session'da cart yönetimi
- Cart class ile OOP interface

### 4. **Contact Guard**
- ThreadMessage.raw_text → contact_guard.check() → redacted_text
- Email/telefon/sosyal medya maskeleme

### 5. **Double-Entry Ledger**
- LedgerEntry ile platform+seller para akışı
- DR/CR pattern ile muhasebe uyumlu

### 6. **Idempotent Webhooks**
- WebhookEvent.dedupe_key → Aynı event tekrar işlenmesin

### 7. **Feature Flags**
- core.context_processors.feature_flags → Template'de özellik kontrolü
- Env var ile feature enable/disable

---

## 🔍 MODEL İLİŞKİ TABLOSU

| Model | İlişkiler | İlişki Tipi |
|-------|-----------|-------------|
| User | → Address | 1:N (ForeignKey) |
| User | → VerifiedSeller | 1:1 (OneToOne) |
| User | → Store (owner) | 1:N (ForeignKey) |
| User | → Order (buyer) | 1:N (ForeignKey) |
| User | → Review | 1:N (ForeignKey) |
| User | → Favorite | 1:N (ForeignKey) |
| User | → Report (reporter) | 1:N (ForeignKey) |
| User | → Ban | 1:N (ForeignKey) |
| User | → SavedSearch | 1:N (ForeignKey) |
| Store | → Listing | 1:N (ForeignKey) |
| Store | → StorePolicy | 1:1 (OneToOne) |
| Store | → LedgerEntry | 1:N (ForeignKey) |
| Category | → Product | 1:N (ForeignKey) |
| Category | → Category (parent) | Self FK |
| Product | → Listing | 1:N (ForeignKey) |
| Listing | → ListingImage | 1:N (ForeignKey) |
| Listing | → Favorite | 1:N (ForeignKey) |
| Listing | → Review | 1:N (ForeignKey) |
| Listing | → Thread | 1:N (ForeignKey) |
| Listing | → PricePoint | 1:N (ForeignKey) |
| Order | → OrderItem | 1:N (ForeignKey) |
| Order | → Payment | 1:1 (OneToOne) |
| Order | → LedgerEntry | 1:N (ForeignKey) |
| Order | → RefundRequest | 1:N (ForeignKey) |
| Payment | → PaymentTransaction | 1:N (ForeignKey) |
| Thread | → ThreadMessage | 1:N (ForeignKey) |
| Report | → ModerationAction | 1:N (ForeignKey) |

---

## 🎯 ÖNEMLİ NOTLAR

### Güvenlik:
- **Listing ownership**: Listing edit/delete için store ownership kontrolü gerekli
- **Order visibility**: Buyer sadece kendi siparişlerini görmeli
- **Messaging**: Thread'e erişim sadece buyer+seller'a açık
- **Admin URL**: `/admin/` default (DEĞİŞTİRİLMELİ - güvenlik riski)

### Performans:
- **select_related/prefetch_related**: N+1 query problemini önlemek için
- **DB Indexes**: Kritik FK ve search field'lerde index var
- **Template caching**: Prod'da cached loader aktif

### Eksiklikler:
- **shipping** modülü boş (gelecek feature)
- **dashboards** modülü view-only (model yok)
- **Rate limiting**: Login/messaging için rate limit önerilir

---

## 📝 SONUÇ

**Mimari Kalitesi**: ✅ İyi organize, Django best practices uyumlu  
**Model İlişkileri**: ✅ Sağlam, FK/O2O/M2M doğru kullanılmış  
**Modüler Yapı**: ✅ Her app tek sorumluluk prensibi  
**Risk Alanları**: ⚠️ Admin URL default, rate limiting yok

**Öneriler**:
1. Admin URL'i değiştir
2. Rate limiting ekle (messaging, login)
3. shipping modülü için plan yap
4. Performans: Kritik query'lerde select_related kullan

---

**Hazırlayan**: AI Assistant  
**Tarih**: 2025-10-20  
**Durum**: TAMAMLANDI ✅


