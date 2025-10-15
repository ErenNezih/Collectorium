# 🔧 COLLECTORIUM - TEKNİK DERİN DALIŞ DOKÜMANTASYONU

**Bölüm:** 2/10 - Django Uygulamaları ve Model Yapısı  
**Tarih:** 15 Ekim 2025

---

## 4. DJANGO UYGULAMALARI DETAYLI ANALİZ

### 4.1 `accounts` - Kullanıcı Yönetimi Uygulaması

#### 📋 Genel Bakış
Kullanıcı kimlik doğrulama, profil yönetimi ve Google OAuth entegrasyonunu yöneten çekirdek uygulama.

#### 🗂️ Models (`accounts/models.py`)

##### **User Model (Custom AbstractUser)**
```python
class User(AbstractUser):
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="buyer")
    store_name = models.CharField(max_length=120, blank=True, null=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
```

**Özellikler:**
- Django'nun AbstractUser'ını extend eder
- 3 rol: `buyer`, `seller`, `admin`
- `@property full_name`: Ad + Soyad veya username döner
- Tüm Django auth özellikleri mevcut (groups, permissions, vb.)

**İlişkiler:**
- `owned_stores` → Store modeli (1:N)
- `orders` → Order modeli (1:N)
- `reviews` → Review modeli (1:N)
- `addresses` → Address modeli (1:N)
- `favorites` → Favorite modeli (1:N)

##### **Address Model**
```python
class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    address_title = models.CharField(max_length=100, help_text="Örn: Ev, İş")
    country = models.CharField(max_length=100, default="Türkiye")
    city = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    full_address = models.TextField()
    postal_code = models.CharField(max_length=10, blank=True, null=True)
    is_default = models.BooleanField(default=False)
```

**Özellikler:**
- Kullanıcı başına çoklu adres desteği
- `is_default` ile varsayılan adres sistemi
- `save()` override: Yeni default adres belirlendiğinde diğerlerini günceller

#### 🎯 Views (`accounts/views.py`)

| View | Tip | URL | Açıklama |
|------|-----|-----|----------|
| `profile` | FBV | `/account/profile/` | Kullanıcı profil sayfası |
| `profile_edit` | FBV | `/account/profile/edit/` | Profil düzenleme |
| `change_password` | FBV | `/account/profile/change-password/` | Şifre değiştirme |
| `my_orders` | FBV | `/account/orders/` | Siparişler + pagination |
| `my_reviews` | FBV | `/account/reviews/` | Yorumlar |
| `my_favorites` | FBV | `/account/favorites/` | Favori ilanlar |
| `MyListingsView` | CBV (ListView) | `/account/my-listings/` | Satıcının ilanları |
| `UserDetailView` | CBV (DetailView) | `/account/user/<username>/` | Public profil |
| `google_onboarding_complete` | FBV | `/accounts/google/signup/complete/` | ⭐ Özel Google onboarding |

#### 🔌 Adapters (`accounts/adapters.py`)

**CustomSocialAccountAdapter**
```python
class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        if sociallogin.is_existing:
            return  # Eski kullanıcı - normal giriş
        
        # Yeni kullanıcı - Google verilerini session'a kaydet
        request.session['google_email'] = sociallogin.account.extra_data['email']
        # ... diğer veriler
        
        # Özel onboarding'e yönlendir
        raise ImmediateHttpResponse(
            HttpResponseRedirect(reverse('google_onboarding_complete'))
        )
```

**Akış:**
1. Google'dan gelen kullanıcı kontrolü
2. Yeni kullanıcıysa → Session'a Google verileri kaydedilir
3. `ImmediateHttpResponse` ile onboarding sayfasına yönlendirme
4. Onboarding sayfasında ek bilgiler toplanır (username, phone, address)
5. User + Address + SocialAccount kaydı oluşturulur
6. Otomatik giriş yapılır

#### 📝 Forms (`accounts/forms.py`)

**GoogleOnboardingForm**
- `username` - Unique, doğrulama var
- `phone` - Format doğrulama
- `address_title`, `city`, `district`, `full_address`, `postal_code`
- `role` - RadioSelect widget (buyer/seller)
- `phone_verified` - Hidden field (Alpine.js ile client-side kontrol)

**Custom Validation:**
```python
def clean(self):
    cleaned_data = super().clean()
    phone_verified = cleaned_data.get('phone_verified')
    if not phone_verified:
        raise forms.ValidationError('Lütfen telefon numaranızı onaylayın.')
    return cleaned_data
```

#### 🔧 Signals (`accounts/signals.py`)

**Otomatik Mağaza Oluşturma**
```python
@receiver(post_save, sender=User)
def create_store_for_seller(sender, instance, created, **kwargs):
    if created and instance.role == 'seller':
        Store.objects.get_or_create(
            owner=instance,
            defaults={
                'name': f"{instance.username}'s Store",
                'slug': slugify(f"{instance.username}-store"),
                'bio': "Yeni mağazam. Hoş geldiniz!"
            }
        )
```

**Ne Zaman Tetiklenir:**
- Yeni seller kaydı yapıldığında
- Seller rolüne geçiş yapıldığında

#### 🛡️ Mixins (`accounts/mixins.py`)

**SellerRequiredMixin**
```python
class SellerRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if request.user.role != 'seller':
            messages.error(request, 'Bu sayfaya sadece satıcılar erişebilir.')
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)
```

**Kullanım:** İlan CRUD view'larında seller olma kontrolü

#### ⚙️ Management Commands

**setup_google_oauth.py**
```bash
python manage.py setup_google_oauth
```

**Ne Yapar:**
- Site nesnesini oluşturur (SITE_ID = 1)
- Domain'i ayarlar (127.0.0.1:8000)
- CEO'ya adım adım Google API kurulum talimatları verir

---

### 4.2 `stores` - Mağaza Yönetimi

#### 🗂️ Model

```python
class Store(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_stores')
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=120, unique=True)
    bio = models.TextField(blank=True, null=True)
    logo = models.ImageField(upload_to='store_logos/', blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

**Özellikler:**
- Her seller'ın bir mağazası olabilir (signal ile otomatik oluşur)
- `is_verified`: Admin tarafından onaylı mağazalar
- `slug`: SEO-friendly URL

**İlişkiler:**
- `owner` → User (N:1)
- `listings` → Listing (1:N)

#### 🎯 Views

| View | Açıklama |
|------|----------|
| `stores_list` | Doğrulanmış mağazalar + arama + pagination |
| `store_detail` | Mağaza profil + ilanları |

**stores_list Özellikleri:**
```python
stores = Store.objects.filter(is_verified=True).annotate(
    listing_count=Count('listings', filter=Q(listings__is_active=True))
).order_by('-created_at')
```
- Sadece doğrulanmış mağazaları gösterir
- Her mağazanın aktif ilan sayısını annotate eder
- Arama desteği (name, bio)

---

### 4.3 `listings` - İlan Yönetimi

#### 🗂️ Models

##### **Listing Model**
```python
class Listing(models.Model):
    CONDITION_CHOICES = [
        ('new', 'Yeni'),
        ('like_new', 'Sıfıra Yakın'),
        ('good', 'İyi'),
        ('fair', 'Orta'),
        ('poor', 'Kötü'),
    ]
    
    store = models.ForeignKey('stores.Store', on_delete=models.CASCADE)
    product = models.ForeignKey('catalog.Product', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='TRY')
    condition = models.CharField(max_length=10, choices=CONDITION_CHOICES)
    stock = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)
```

**Önemli Metodlar:**
```python
def get_primary_image(self):
    primary = self.images.filter(is_primary=True).first()
    if primary:
        return primary
    return self.images.first()
```

##### **ListingImage Model**
```python
class ListingImage(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='listing_images/')
    alt_text = models.CharField(max_length=200, blank=True, null=True)
    is_primary = models.BooleanField(default=False)
```

**Özellikler:**
- Bir ilana çoklu resim
- `is_primary`: Ana görsel belirleme
- Ordering: Primary olanlar önce

##### **Favorite Model**
```python
class Favorite(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'listing']
```

**Özellikler:**
- Kullanıcı başına bir ilana bir favori (unique_together)
- İleride "favori ilanlarım" sayfası için kullanılacak

#### 🎯 Views (CRUD)

**ListingCreateView (CBV - CreateView)**
```python
class ListingCreateView(LoginRequiredMixin, SellerRequiredMixin, CreateView):
    model = Listing
    form_class = ListingForm
    template_name = 'listings/listing_form.html'
    
    def form_valid(self, form):
        form.instance.store = self.request.user.store  # Otomatik mağaza ataması
        # Resim yükleme
        images = self.request.FILES.getlist('images')
        for image in images:
            ListingImage.objects.create(listing=self.object, image=image)
        messages.success(self.request, "İlanınız başarıyla oluşturuldu.")
        return redirect('my_listings')
```

**Güvenlik Özellikleri:**
- `LoginRequiredMixin`: Giriş yapmış kullanıcı kontrolü
- `SellerRequiredMixin`: Seller rolü kontrolü
- `ListingOwnerRequiredMixin` (Update/Delete): Sadece sahibi değiştirebilir

**ListingDetailView**
```python
class ListingDetailView(DetailView):
    model = Listing
    template_name = 'listing_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart_add_form'] = CartAddListingForm()  # Sepete ekle formu
        return context
```

#### 📝 Forms

**ListingForm**
- Tüm Listing alanları (title, description, price, condition, stock)
- Product seçimi (dropdown)
- Resim yükleme (ImageUploadForm)

#### 🛡️ Mixins

**ListingOwnerRequiredMixin**
```python
class ListingOwnerRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        listing = self.get_object()
        if listing.store.owner != request.user:
            messages.error(request, 'Bu ilana erişim yetkiniz yok.')
            return redirect('my_listings')
        return super().dispatch(request, *args, **kwargs)
```

---

### 4.4 `catalog` - Ürün Kataloğu

#### 🗂️ Models

##### **Category Model**
```python
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='category_images/', blank=True, null=True)
```

**Özellikler:**
- Self-referencing foreign key (hierarchical kategoriler)
- Örnek: Kategori: "TCG" → Alt Kategori: "Pokemon", "Yu-Gi-Oh"

##### **Product Model**
```python
class Product(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    
    class Meta:
        unique_together = ['name', 'brand']
```

**Özellikler:**
- Her ürün bir kategoriye ait
- `name + brand` kombinasyonu unique (örn: "Pikachu" + "Pokemon")
- Ürünler ilanlardan bağımsız (bir ürünün birden fazla ilanı olabilir)

---

### 4.5 `cart` - Alışveriş Sepeti

#### 🛒 Cart Sınıfı (`cart/cart.py`)

**Session-Based Cart Implementasyonu:**

```python
class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
```

**Temel Metodlar:**

| Metod | Açıklama |
|-------|----------|
| `add(listing, quantity, override_quantity)` | Ürün ekle/güncelle |
| `remove(listing)` | Ürün çıkar |
| `__iter__()` | Sepetteki ürünler üzerinde döngü |
| `__len__()` | Toplam ürün sayısı |
| `get_total_price()` | Toplam tutar |
| `clear()` | Sepeti temizle |

**Önemli Özellik:**
```python
def __iter__(self):
    listing_ids = self.cart.keys()
    listings = Listing.objects.filter(id__in=listing_ids)
    cart = self.cart.copy()
    for listing in listings:
        cart[str(listing.id)]['listing'] = listing
    
    for item in cart.values():
        item['price'] = Decimal(item['price'])
        item['total_price'] = item['price'] * item['quantity']
        yield item
```
- Session'daki ID'lerden Listing nesnelerini çeker
- Toplam fiyat hesaplama
- Generator pattern kullanımı

#### 🎯 Views

| View | Açıklama |
|------|----------|
| `cart_detail` | Sepet sayfası |
| `cart_add` | Sepete ürün ekle (HTMX ile asenkron) |
| `cart_remove` | Sepetten çıkar |

**cart_add Örneği:**
```python
def cart_add(request, listing_id):
    cart = Cart(request)
    listing = get_object_or_404(Listing, id=listing_id)
    form = CartAddListingForm(request.POST)
    
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(listing=listing, quantity=cd['quantity'], 
                override_quantity=cd['override'])
        messages.success(request, f'"{listing.title}" sepete eklendi.')
    
    return redirect('cart:cart_detail')
```

#### 🔌 Context Processors

```python
def cart(request):
    return {'cart': Cart(request)}
```

**Ne İşe Yarar:**
- Tüm template'lerde `{{ cart }}` kullanılabilir
- Header'da sepet badge'i için gerekli
- Global erişim

---

### 4.6 `orders` - Sipariş Yönetimi

#### 🗂️ Models

##### **Order Model**
```python
class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Beklemede'),
        ('paid', 'Ödendi'),
        ('shipped', 'Kargoya Verildi'),
        ('delivered', 'Teslim Edildi'),
        ('cancelled', 'İptal Edildi'),
        ('refunded', 'İade Edildi'),
    ]
    
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='TRY')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    shipping_address = models.TextField()
    notes = models.TextField(blank=True, null=True)
```

##### **OrderItem Model**
```python
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    listing = models.ForeignKey('listings.Listing', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price_snapshot = models.DecimalField(max_digits=10, decimal_places=2)
```

**Önemli:** `price_snapshot` - Sipariş anındaki fiyat kaydedilir (fiyat değişse bile sipariş etkilenmez)

#### 🎯 Views

**order_create (Checkout)**
```python
def order_create(request):
    cart = Cart(request)
    
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            # Order oluştur
            order = form.save(commit=False)
            order.buyer = request.user
            order.total = cart.get_total_price()
            order.save()
            
            # OrderItem'ları oluştur
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    listing=item['listing'],
                    quantity=item['quantity'],
                    price_snapshot=item['price']
                )
            
            # Sepeti temizle
            cart.clear()
            
            messages.success(request, f'Siparişiniz oluşturuldu! Sipariş numaranız: #{order.id}')
            return render(request, 'orders/order_created.html', {'order': order})
    
    else:
        form = OrderCreateForm()
    
    return render(request, 'orders/checkout.html', {'cart': cart, 'form': form})
```

**Akış:**
1. Kullanıcı checkout sayfasına gider
2. Adres formu doldurur
3. Order oluşturulur (buyer, total, shipping_address)
4. Sepetteki her ürün için OrderItem oluşturulur
5. Sepet temizlenir
6. "Sipariş Oluşturuldu" sayfası gösterilir

---

**Dokümantasyon devam ediyor... (Sayfa 2/10)**

*Not: Sonraki bölümlerde `reviews`, `core`, operasyon detayları ve deployment rehberi yer alacaktır.*
