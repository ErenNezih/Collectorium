from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash, login
from django.contrib.auth.forms import PasswordChangeForm
from django.core.paginator import Paginator
from django.views.generic import ListView, DetailView
from .models import User, Address
from listings.models import Listing
from orders.models import Order
from reviews.models import Review
from .mixins import SellerRequiredMixin
from .forms import GoogleOnboardingForm
from allauth.socialaccount.models import SocialAccount
from stores.models import Store


@login_required
def profile(request):
    """Kullanıcı profil sayfası"""
    user = request.user
    
    # Kullanıcının sahip olduğu mağaza
    try:
        store = user.owned_stores.first()
    except:
        store = None
    
    # Kullanıcının siparişleri
    orders = Order.objects.filter(buyer=user).order_by('-created_at')[:5]
    
    # Kullanıcının yorumları
    reviews = Review.objects.filter(user=user).order_by('-created_at')[:5]
    
    # Kullanıcının favorileri (eğer Favorite modeli varsa)
    # favorites = Favorite.objects.filter(user=user).select_related('listing')[:5]
    
    context = {
        'user': user,
        'store': store,
        'orders': orders,
        'reviews': reviews,
        # 'favorites': favorites,
    }
    return render(request, 'accounts/profile.html', context)


@login_required
def profile_edit(request):
    """Kullanıcı profil düzenleme"""
    if request.method == 'POST':
        user = request.user
        
        # Temel bilgiler
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.email = request.POST.get('email', '')
        
        # Avatar
        if 'avatar' in request.FILES:
            user.avatar = request.FILES['avatar']
        
        # Store bilgileri
        if user.role == 'seller':
            store_name = request.POST.get('store_name', '')
            if store_name:
                user.store_name = store_name
        
        user.save()
        messages.success(request, 'Profil bilgileriniz başarıyla güncellendi!')
        return redirect('profile')
    
    return render(request, 'accounts/profile_edit.html')


@login_required
def change_password(request):
    """Şifre değiştirme"""
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Şifreniz başarıyla değiştirildi.')
            return redirect('profile')
        else:
            messages.error(request, 'Şifre değiştirme sırasında hata oluştu.')
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, 'accounts/change_password.html', {'form': form})


@login_required
def my_orders(request):
    """Kullanıcının siparişleri"""
    orders = Order.objects.filter(buyer=request.user).order_by('-created_at')
    
    # Filtreleme
    status_filter = request.GET.get('status')
    if status_filter:
        orders = orders.filter(status=status_filter)
    
    paginator = Paginator(orders, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'orders': page_obj,
        'status_filter': status_filter,
    }
    return render(request, 'accounts/my_orders.html', context)


@login_required
def my_reviews(request):
    """Kullanıcının yorumları"""
    reviews = Review.objects.filter(user=request.user).select_related('listing').order_by('-created_at')
    
    paginator = Paginator(reviews, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'accounts/my_reviews.html', {'page_obj': page_obj})


@login_required
def my_favorites(request):
    """Kullanıcının favorileri"""
    # Favoriler modeli henüz yok, placeholder
    favorites = []
    
    paginator = Paginator(favorites, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'accounts/my_favorites.html', {'page_obj': page_obj})


class UserDetailView(DetailView):
    """Kullanıcı profil sayfası (public)"""
    model = User
    template_name = 'accounts/user_detail.html'
    context_object_name = 'profile_user'
    slug_field = 'username'
    slug_url_kwarg = 'username'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.object
        
        # Kullanıcının mağazası
        try:
            store = user.owned_stores.first()
        except:
            store = None
        
        # Kullanıcının ilanları (eğer satıcıysa)
        if store:
            listings = Listing.objects.filter(store=store, is_active=True).order_by('-created_at')[:8]
        else:
            listings = []
        
        # Kullanıcının yorumları
        reviews = Review.objects.filter(user=user).order_by('-created_at')[:5]
        
        context.update({
            'store': store,
            'listings': listings,
            'reviews': reviews,
        })
        return context


class MyListingsView(LoginRequiredMixin, SellerRequiredMixin, ListView):
    model = Listing
    template_name = 'accounts/my_listings.html'
    context_object_name = 'listings'
    paginate_by = 10

    def get_queryset(self):
        # Sadece giriş yapmış olan satıcının mağazasına ait ilanları listele
        store = self.request.user.owned_stores.first()
        return Listing.objects.filter(store=store).order_by('-created_at')


# =============================================================================
# KEYSTONE OPERASYONU - GOOGLE ONBOARDING
# =============================================================================

def google_onboarding_complete(request):
    """
    Google ile giriş yapan yeni kullanıcılar için özel onboarding sayfası.
    
    Bu view, Google'dan gelen temel bilgileri (email, isim) session'dan alır,
    kullanıcıdan ek bilgiler (username, telefon, adres) toplar ve
    tam bir User + Address kaydı oluşturarak süreci tamamlar.
    
    Akış:
    1. Session'da Google verilerini kontrol et
    2. GET → Formu göster (Google bilgileri pre-fill)
    3. POST → Telefon onayını kontrol et, User + Address oluştur, giriş yap
    """
    
    # Session kontrolü - Google'dan gelip gelmediğini doğrula
    if not request.session.get('pending_sociallogin'):
        messages.error(request, 'Geçersiz erişim. Lütfen Google ile giriş yapın.')
        return redirect('account_login')
    
    if request.method == 'POST':
        form = GoogleOnboardingForm(request.POST)
        
        if form.is_valid():
            # Session'dan Google verilerini al
            google_email = request.session.get('google_email')
            google_first_name = request.session.get('google_first_name', '')
            google_last_name = request.session.get('google_last_name', '')
            google_uid = request.session.get('google_uid')
            google_provider = request.session.get('google_provider', 'google')
            
            # Form'dan yeni verileri al
            username = form.cleaned_data['username']
            phone = form.cleaned_data['phone']
            role = form.cleaned_data['role']
            
            try:
                # 1. YENİ USER OLUŞTUR
                user = User.objects.create_user(
                    username=username,
                    email=google_email,
                    first_name=google_first_name,
                    last_name=google_last_name,
                    role=role,
                    phone=phone
                )
                
                # 2. ADRES OLUŞTUR
                Address.objects.create(
                    user=user,
                    address_title=form.cleaned_data['address_title'],
                    city=form.cleaned_data['city'],
                    district=form.cleaned_data['district'],
                    full_address=form.cleaned_data['full_address'],
                    postal_code=form.cleaned_data.get('postal_code', ''),
                    is_default=True
                )
                
                # 3. GOOGLE HESABI İLE BAĞLA
                SocialAccount.objects.create(
                    user=user,
                    provider=google_provider,
                    uid=google_uid,
                    extra_data={
                        'email': google_email,
                        'given_name': google_first_name,
                        'family_name': google_last_name,
                    }
                )
                
                # 4. EĞER SATICI İSE, MAĞAZA OLUŞTUR
                if role == 'seller':
                    Store.objects.create(
                        owner=user,
                        name=f"{username}'s Store",
                        slug=f"{username}-store",
                        bio="Hoş geldiniz! Mağazamı yeni açtım."
                    )
                
                # 5. SESSION'I TEMİZLE
                request.session.pop('pending_sociallogin', None)
                request.session.pop('google_email', None)
                request.session.pop('google_first_name', None)
                request.session.pop('google_last_name', None)
                request.session.pop('google_full_name', None)
                request.session.pop('google_uid', None)
                request.session.pop('google_provider', None)
                
                # 6. KULLANICI GİRİŞİNİ YAP
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                
                # 7. HOŞ GELDİN MESAJI
                messages.success(
                    request,
                    f'Hoş geldiniz, {user.first_name}! 🎉 Hesabınız başarıyla oluşturuldu.'
                )
                
                # 8. ANA SAYFAYA YÖNLENDİR
                return redirect('home')
                
            except Exception as e:
                messages.error(
                    request,
                    f'Bir hata oluştu: {str(e)}. Lütfen tekrar deneyin.'
                )
                form = GoogleOnboardingForm()
        
    else:
        # GET REQUEST - Formu göster
        form = GoogleOnboardingForm()
    
    # Session'dan Google bilgilerini context'e ekle (template'de göstermek için)
    context = {
        'form': form,
        'google_email': request.session.get('google_email'),
        'google_name': request.session.get('google_full_name', ''),
    }
    
    return render(request, 'accounts/google_onboarding.html', context)