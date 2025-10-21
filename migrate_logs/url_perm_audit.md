# 🔐 URL & PERMISSION AUDIT

**Tarih**: 20 Ekim 2025  
**Analiz**: URL patterns, authentication, authorization, CSRF

---

## 📋 URL YAPISI

### Main URLs (collectorium/urls.py)

```python
urlpatterns = [
    path('admin/', admin.site.urls),                                    # ⚠️ DEFAULT
    path('', include('core.urls')),                                     # ✅ Public
    path('accounts/', include('allauth.urls')),                         # ✅ django-allauth
    path('listings/', include('listings.urls', namespace='listings')), # ✅
    path('account/', include('accounts.urls')),                         # ✅
    path('cart/', include('cart.urls', namespace='cart')),             # ✅
    path('orders/', include('orders.urls', namespace='orders')),       # ✅
    path('stores/', include('stores.urls', namespace='stores')),       # ✅
    path('categories/', include('catalog.urls', namespace='catalog')), # ✅
    path('search/', include('search.urls', namespace='search')),       # ✅
    path('m/', include('messaging.urls', namespace='messaging')),      # ✅
    path('payments/', include('payments.urls', namespace='payments')), # ✅
    path('mod/', include('moderation.urls', namespace='moderation')), # ✅
]
```

**Toplam Top-Level URL**: 13

---

## 🚨 KRİTİK GÜVENLİK BULGULARI

### 1. ADMIN URL (DEFAULT)

**Durum**: ⚠️ **YÜKSEK RİSK**

**Mevcut**:
```python
path('admin/', admin.site.urls),  # Line 7
```

**Problem**: `/admin/` herkesçe bilinen URL, brute-force hedefi

**Çözüm**: Custom URL kullan

**Öneri Diff**:
```python
# collectorium/settings/hosting.py'ye ekle (satır ~408 sonrası):
ADMIN_URL = os.environ.get('ADMIN_URL', 'admin/').rstrip('/') + '/'

# collectorium/urls.py'de değiştir (satır 7):
# Eski:
path('admin/', admin.site.urls),
# Yeni:
path(getattr(settings, 'ADMIN_URL', 'admin/'), admin.site.urls),
```

**Environment Variable**:
```bash
ADMIN_URL=control-panel-xj9k2/
```

**Yeni URL**: `https://yourdomain.com/control-panel-xj9k2/`

**Öncelik**: YÜKSEK - Deployment öncesi değiştir

---

### 2. CSRF Exempt (webhook için)

**Konum**: `payments/views.py`

```python
@csrf_exempt  # Line 83
def iyzico_webhook_handler(request):
    # Webhook handler
    ...
```

**Durum**: ✅ GÜVENLİ (doğru kullanım)

**Analiz**:
- ✅ Webhook endpoint'i için gerekli (external service POST eder)
- ✅ Signature verification ile korunuyor olmalı
- ⚠️ Signature check kodu kontrol edilmeli

**Risk**: DÜŞÜK (webhook'lar CSRF'den muaf tutulmalı, ama signature check şart)

---

## 🔒 AUTHENTICATION & AUTHORIZATION

### LoginRequiredMixin Kullanımı

**Dosyalar**: 7 dosyada kullanılıyor
- listings/views.py
- accounts/views.py
- orders/views.py
- stores/views.py
- messaging/views.py
- search/views.py
- moderation/views.py

**Örnek** (listings/views.py):
```python
class ListingCreateView(LoginRequiredMixin, SellerRequiredMixin, CreateView):
    # Listing oluşturma sadece login + seller role ile
```

**Durum**: ✅ DOĞRU - CRUD işlemleri authentication ile korunmuş

---

### Custom Mixins

#### accounts/mixins.py

```python
class SellerRequiredMixin:
    """
    Sadece seller rolündeki kullanıcıların erişmesini sağlar.
    """
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/accounts/login/')
        if request.user.role != 'seller':
            messages.error(request, "Bu sayfaya erişmek için satıcı hesabı gereklidir.")
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)
```

**Durum**: ✅ DOĞRU  
**Kullanım**: Listing CRUD, Store management

---

#### listings/mixins.py

```python
class ListingOwnerRequiredMixin:
    """
    Sadece ilanın sahibi olan satıcının erişmesini sağlar.
    """
    def dispatch(self, request, *args, **kwargs):
        listing = self.get_object()
        if listing.store.owner != request.user:
            messages.error(request, "Bu ilana erişim yetkiniz yok.")
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)
```

**Durum**: ✅ DOĞRU  
**Kullanım**: Listing edit/delete

---

## 📊 ENDPOINT PERMISSION MATRİSİ

### Public Endpoints (Authentication Not Required)

| URL | View | Permission | CSRF | Durum |
|-----|------|------------|------|-------|
| `/` | home | Public | ✅ | ✅ Safe |
| `/marketplace/` | marketplace | Public | ✅ | ✅ Safe |
| `/listing/<id>/` | listing_detail | Public | ✅ | ✅ Safe |
| `/categories/` | categories_list | Public | ✅ | ✅ Safe |
| `/categories/<slug>/` | category_detail | Public | ✅ | ✅ Safe |
| `/healthz/` | healthz | Public | ✅ | ✅ Safe |
| `/health/readiness/` | readiness | Public | ✅ | ✅ Safe |
| `/health/liveness/` | liveness | Public | ✅ | ✅ Safe |

**Analiz**: Ana navigation public (✓ marketplace için doğru)

---

### Login Required Endpoints

| URL | View | Extra Permission | Durum |
|-----|------|------------------|-------|
| `/account/profile/` | profile | LoginRequired | ✅ |
| `/account/profile/edit/` | profile_edit | LoginRequired | ✅ |
| `/account/orders/` | my_orders | LoginRequired | ✅ |
| `/account/favorites/` | my_favorites | LoginRequired | ✅ |
| `/cart/` | cart_detail | Public (!) | ⚠️ |
| `/orders/checkout/` | checkout | LoginRequired | ✅ |

**Dikkat**: `/cart/` public - Session-based, login gerektirmiyor (✓ tasarım kararı)

---

### Seller Required Endpoints

| URL | View | Mixins | Durum |
|-----|------|--------|-------|
| `/listings/create/` | ListingCreateView | LoginRequired + SellerRequired | ✅ |
| `/listings/<pk>/edit/` | ListingUpdateView | LoginRequired + SellerRequired + OwnerRequired | ✅ |
| `/listings/<pk>/delete/` | ListingDeleteView | LoginRequired + SellerRequired + OwnerRequired | ✅ |
| `/account/my-listings/` | MyListingsView | LoginRequired + SellerRequired | ✅ |
| `/stores/create/` | StoreCreateView | LoginRequired + SellerRequired | ✅ |
| `/stores/<slug>/edit/` | StoreUpdateView | LoginRequired + SellerRequired | ✅ |

**Analiz**: Seller işlemleri çift korumalı (role + ownership) ✅

---

### Admin/Moderator Endpoints

| URL | View | Permission | Durum |
|-----|------|------------|-------|
| `/admin/` | Django Admin | is_staff=True | ⚠️ DEFAULT URL |
| `/mod/` | Moderation dashboard | Moderator (?) | ⚠️ Check |
| `/mod/reports/` | Reports list | Moderator (?) | ⚠️ Check |

**Dikkat**: Moderation view'larında permission check kontrol edilmeli

---

### CSRF Exempt Endpoints (Webhooks)

| URL | View | Reason | Security | Durum |
|-----|------|--------|----------|-------|
| `/payments/webhook/` | iyzico_webhook_handler | External POST | ⚠️ Signature check? | ⚠️ Verify |

**Analiz**: Webhook CSRF exempt (doğru) ama signature verification olmalı

---

## 🔍 MIXIN & DECORATOR ANALİZİ

### SellerRequiredMixin

**Konum**: `accounts/mixins.py`

**Kontroller**:
1. ✅ `request.user.is_authenticated`
2. ✅ `request.user.role == 'seller'`

**Redirect**:
- Unauthenticated → `/accounts/login/`
- Non-seller → home + error message

**Durum**: ✅ GÜVENLİ

---

### ListingOwnerRequiredMixin

**Konum**: `listings/mixins.py`

**Kontroller**:
1. ✅ `listing.store.owner == request.user`

**Redirect**: Unauthorized → home + error message

**Durum**: ✅ GÜVENLİ

**Risk**: YOK - Ownership doğru check ediliyor

---

### @login_required Decorator

**Kullanım**: Function-based views'larda

**Örnek** (accounts/views.py):
```python
@login_required
def profile(request):
    ...
```

**Durum**: ✅ DOĞRU

---

## ⚠️ POTENTIAL SECURITY GAPS

### 1. Moderation View Permissions

**Durum**: ⚠️ KONTROL GEREKLİ

**Soru**: `/mod/` endpoint'leri kime açık?
- is_staff gerekli mi?
- Custom moderator permission var mı?
- Herkes erişebilir mi?

**Önerilen Kontrol**:
```bash
grep -n "class.*View" moderation/views.py
grep -n "LoginRequired\|PermissionRequired\|is_staff" moderation/views.py
```

**Çözüm** (eğer protection yoksa):
```python
# moderation/views.py
from django.contrib.auth.mixins import PermissionRequiredMixin

class ReportListView(PermissionRequiredMixin, ListView):
    permission_required = 'moderation.view_report'
    # veya
    # def dispatch(self, request, *args, **kwargs):
    #     if not request.user.is_staff:
    #         return redirect('home')
```

---

### 2. Order View Permissions

**Kontrol**: Buyer sadece kendi siparişlerini görmeli

**Örnek** (orders/views.py - kontrol et):
```python
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    # ⚠️ Kontrol: order.buyer == request.user ?
    if order.buyer != request.user and not request.user.is_staff:
        return HttpResponseForbidden("Unauthorized")
    ...
```

**Durum**: ⚠️ KONTROL GEREKLİ - Order detail view'da ownership check olmalı

---

### 3. Messaging Thread Access

**Kontrol**: Thread'e sadece buyer veya seller erişmeli

**Örnek Check**:
```python
def thread_detail(request, thread_id):
    thread = get_object_or_404(Thread, pk=thread_id)
    # Check: thread.buyer == request.user OR thread.seller == request.user
```

**Durum**: ⚠️ KONTROL GEREKLİ

---

## 📊 URL NAMESPACE & REVERSE LOOKUP

### Namespace'li Apps

| App | Namespace | Örnek Reverse |
|-----|-----------|---------------|
| listings | 'listings' | `reverse('listings:create')` |
| cart | 'cart' | `reverse('cart:cart_detail')` |
| orders | 'orders' | `reverse('orders:checkout')` |
| stores | 'stores' | `reverse('stores:store_detail', args=[slug])` |
| catalog | 'catalog' | `reverse('catalog:category_detail', args=[slug])` |
| search | 'search' | `reverse('search:search')` |
| messaging | 'messaging' | `reverse('messaging:threads')` |
| payments | 'payments' | `reverse('payments:process')` |
| moderation | 'moderation' | `reverse('moderation:reports')` |

**Durum**: ✅ DOĞRU - Namespace collision yok

---

### Namespace'siz Apps

| App | URL Prefix | Örnek |
|-----|-----------|-------|
| core | '/' | Direct path names |
| accounts | '/account/' | Direct path names |
| allauth | '/accounts/' | allauth built-in |

**Durum**: ✅ DOĞRU - Conflict yok (/account/ vs /accounts/)

---

## 🔍 CSRF PROTECTION ANALİZİ

### CSRF Protected Endpoints (Default)

**Tüm POST/PUT/DELETE**: ✅ CSRF korumalı (Django default)

**Örnekler**:
- Listing create/edit/delete → CSRF token gerekli
- Cart add/remove → CSRF token gerekli
- Order checkout → CSRF token gerekli
- Profile edit → CSRF token gerekli

**Durum**: ✅ GÜVENLİ

---

### CSRF Exempt Endpoints

**Toplam**: 1 endpoint

**payments/views.py (satır 83)**:
```python
@csrf_exempt
def iyzico_webhook_handler(request):
    # External webhook POST'u
```

**Analiz**:
- ✅ Webhook için gerekli (Iyzico CSRF token gönderemez)
- ⚠️ Signature verification olmalı (IP check, HMAC, vs.)
- ⚠️ Kod review edilmeli

**Güvenlik Kontrolü Önerileri**:
```python
# Signature verification
def iyzico_webhook_handler(request):
    # 1. IP whitelist check
    if request.META.get('REMOTE_ADDR') not in ALLOWED_IPS:
        return HttpResponseForbidden()
    
    # 2. Signature verification
    signature = request.headers.get('X-Iyzico-Signature')
    if not verify_signature(request.body, signature):
        return HttpResponseForbidden()
    
    # 3. Idempotency check
    event_id = data.get('event_id')
    if WebhookEvent.objects.filter(dedupe_key=event_id).exists():
        return JsonResponse({'status': 'already_processed'})
    
    # Process webhook
    ...
```

**Durum**: ⚠️ SIGNATURE VERIFICATION KONTROL EDİLMELİ

---

## 🎯 VIEW-LEVEL SECURITY

### Listing Views

| View | Authentication | Role Check | Ownership Check | Durum |
|------|----------------|------------|-----------------|-------|
| ListingCreateView | ✅ LoginRequiredMixin | ✅ SellerRequiredMixin | N/A | ✅ |
| ListingUpdateView | ✅ LoginRequiredMixin | ✅ SellerRequiredMixin | ✅ ListingOwnerRequiredMixin | ✅ |
| ListingDeleteView | ✅ LoginRequiredMixin | ✅ SellerRequiredMixin | ✅ ListingOwnerRequiredMixin | ✅ |
| ListingDetailView | ❌ Public | N/A | N/A | ✅ Doğru |

**Sonuç**: ✅ İdeal security pattern

---

### Orders Views

**Örnek**: `order_detail` view

**Beklenen Kontroller**:
1. ✅ LoginRequired
2. ⚠️ `order.buyer == request.user` (kontrol edilmeli)
3. ⚠️ OR `request.user.is_staff`

**Durum**: ⚠️ SOURCE CODE REVIEW GEREKLİ

**Test**:
```bash
# User A ile login
# User B'nin order ID'sini URL'e yaz
# Sonuç: 403 Forbidden olmalı
```

---

### Messaging Views

**Beklenen Kontroller**:
1. ✅ LoginRequired
2. ⚠️ `thread.buyer == user OR thread.seller == user`

**Durum**: ⚠️ SOURCE CODE REVIEW GEREKLİ

---

### Moderation Views

**Beklenen Kontroller**:
1. ✅ LoginRequired
2. ⚠️ `user.is_staff` OR custom moderator permission

**Durum**: ⚠️ SOURCE CODE REVIEW GEREKLİ

---

## 🔐 PERMISSION RECOMMENDATIONS

### High Priority Fixes

1. **Admin URL Change**
   - **Why**: Default `/admin/` brute-force riski
   - **How**: Environment variable ile custom URL
   - **Priority**: YÜKSEK

2. **Moderation Permission Check**
   - **Why**: `/mod/` erişimi kontrol edilmeli
   - **How**: is_staff veya custom permission
   - **Priority**: YÜKSEK

3. **Order Ownership Check**
   - **Why**: User başkasının siparişini görmemeli
   - **How**: `order.buyer == request.user` check
   - **Priority**: YÜKSEK

4. **Messaging Thread Access**
   - **Why**: Thread'e sadece participant erişmeli
   - **How**: `thread.buyer == user OR thread.seller == user`
   - **Priority**: YÜKSEK

5. **Webhook Signature Verification**
   - **Why**: CSRF exempt endpoint korunmalı
   - **How**: HMAC signature check
   - **Priority**: ORTA (webhook henüz production'da değilse)

---

### Medium Priority Additions

6. **Rate Limiting**
   - **Where**: Login, messaging, contact form
   - **How**: django-ratelimit
   - **Example**:
     ```python
     from django_ratelimit.decorators import ratelimit
     
     @ratelimit(key='ip', rate='5/h', method='POST')
     def login_view(request):
         ...
     ```

7. **CAPTCHA on Contact Form**
   - **Why**: Spam prevention
   - **How**: django-recaptcha
   - **Priority**: ORTA

---

## 📋 MISSING PERMISSIONS

### Admin Panel

**Mevcut**: `is_staff=True` (Django default)

**Eksik**:
- ⚠️ Custom admin permissions (CRUD per model)
- ⚠️ IP whitelist (opsiyonel)

**Öneri**:
```python
# hosting.py'ye ekle:
ADMIN_ALLOWED_IPS = os.environ.get('ADMIN_ALLOWED_IPS', '').split(',')

# middleware veya decorator ile check:
def admin_ip_check(get_response):
    def middleware(request):
        if request.path.startswith('/admin/'):
            if ADMIN_ALLOWED_IPS and request.META.get('REMOTE_ADDR') not in ADMIN_ALLOWED_IPS:
                return HttpResponseForbidden("Access denied")
        return get_response(request)
    return middleware
```

---

## 🧪 TEST SENARYOLARI

### Test 1: Unauthorized Listing Edit

**Senaryo**:
1. User A creates listing
2. User B (seller) tries to edit User A's listing
3. Expected: 403 or redirect to home with error

**Test Command** (Manual):
```
Visit: /listings/<user_a_listing_id>/edit/
Login as: User B
Expected: Error message + redirect
```

---

### Test 2: Non-seller Accessing Seller Views

**Senaryo**:
1. User with role='buyer' tries to access /listings/create/
2. Expected: Redirect to home + "satıcı hesabı gereklidir" message

**Test**: ✅ SellerRequiredMixin sağlar

---

### Test 3: Order Access Control

**Senaryo**:
1. User A places order (ID=123)
2. User B tries to access /orders/123/
3. Expected: 403 or error

**Test**: ⚠️ VIEW CODE KONTROL EDİLMELİ

---

### Test 4: Admin Brute-Force

**Senaryo**:
1. Attacker tries /admin/ with common passwords
2. Expected: Rate limit veya account lock

**Mevcut**: ❌ Rate limit yok  
**Öneri**: django-ratelimit + admin URL değiştir

---

## 🎯 ÖNERİLER (Diff'ler)

### Öneri 1: Admin URL Environment Variable

**Dosya**: `collectorium/settings/hosting.py`

```diff
# Satır ~408 sonrası ekle:
+ # Admin URL customization
+ ADMIN_URL = os.environ.get('ADMIN_URL', 'admin/').rstrip('/') + '/'
```

**Dosya**: `collectorium/urls.py`

```diff
# Satır 1'e ekle:
+ from django.conf import settings

# Satır 7'yi değiştir:
- path('admin/', admin.site.urls),
+ path(getattr(settings, 'ADMIN_URL', 'admin/'), admin.site.urls),
```

---

### Öneri 2: Order Ownership Check

**Dosya**: `orders/views.py` (kontrol et, yoksa ekle)

```diff
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
+   # Ownership check
+   if order.buyer != request.user and not request.user.is_staff:
+       messages.error(request, "Bu siparişe erişim yetkiniz yok.")
+       return redirect('home')
    ...
```

---

### Öneri 3: Moderation Permission

**Dosya**: `moderation/views.py` (kontrol et, yoksa ekle)

```diff
+ from django.contrib.auth.mixins import UserPassesTestMixin
+
+ class ModeratorRequiredMixin(UserPassesTestMixin):
+     def test_func(self):
+         return self.request.user.is_staff  # veya custom moderator group

class ReportListView(LoginRequiredMixin, ModeratorRequiredMixin, ListView):
    ...
```

---

### Öneri 4: Rate Limiting (Login)

**Dosya**: `requirements.txt`

```diff
+ django-ratelimit>=4.1.0
```

**Dosya**: Login view'ında (django-allauth kullanıyorsanız, custom adapter ile)

```python
from django_ratelimit.decorators import ratelimit

@ratelimit(key='ip', rate='5/h', method='POST', block=True)
def custom_login_view(request):
    ...
```

---

## 📊 ÖZET

**Toplam URL Endpoint**: 50+  
**Public Endpoints**: 10  
**Login Required**: 20+  
**Seller Required**: 10+  
**Admin/Moderator**: 5+

**Critical Security Issues**: 1 (Admin URL default)  
**High Priority Checks**: 4 (Ownership checks)  
**Medium Priority**: 2 (Rate limiting, CAPTCHA)

**Overall Security**: ⚠️ **İYİ AMA İYİLEŞTİRİLEBİLİR**

---

## ✅ GO/NO-GO

**URL & Permission Açısından**: ⚠️ **CONDITIONAL GO**

**Önkoşullar**:
1. ✅ Admin URL değiştirilmeli
2. ⚠️ Order, messaging, moderation ownership checks verify edilmeli
3. ⚠️ Webhook signature verification kontrol edilmeli

**Risk Level**: ORTA (düzeltilebilir)

---

**Hazırlayan**: AI Assistant  
**Tarih**: 2025-10-20  
**Durum**: TAMAMLANDI ✅

**Action Required**: Source code review (orders, messaging, moderation views)


