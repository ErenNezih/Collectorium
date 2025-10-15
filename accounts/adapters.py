"""
Collectorium Custom Social Account Adapter
'Keystone' Operasyonu - Akıllı Onboarding Merkezi

Bu adapter, Google OAuth akışını ele geçirerek yeni ve eski kullanıcıları
akıllıca ayırt eder ve her birine özel bir yolculuk sunar.
"""

from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.shortcuts import redirect
from django.urls import reverse
from allauth.exceptions import ImmediateHttpResponse
from django.http import HttpResponseRedirect


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    """
    Akıllı Yönlendirici - Google OAuth Kontrol Merkezi
    
    Bu sınıf, tüm sosyal giriş akışlarını izler ve yeni kullanıcılar için
    özel onboarding sürecini devreye sokar.
    """
    
    def pre_social_login(self, request, sociallogin):
        """
        Google'dan gelen her kimlik doğrulamanın ilk durağı.
        
        Akış Mantığı:
        1. Gelen sosyal hesaba bağlı bir User var mı kontrol et
        2. User VARSA → Standart akışa devam et (giriş yap)
        3. User YOKSA → Yeni kullanıcı! Onboarding'e yönlendir
        
        Args:
            request: Django HTTP request
            sociallogin: SocialLogin object (Google'dan gelen veriler)
        """
        # Eğer bu sosyal hesap zaten bir kullanıcıya bağlıysa
        if sociallogin.is_existing:
            # Eski kullanıcı - Hiçbir şey yapma, standart giriş devam etsin
            return
        
        # YENİ KULLANICI TESPİT EDİLDİ!
        # Google'dan gelen değerli verileri session'a kaydet
        
        # Email bilgisi
        if sociallogin.account.extra_data.get('email'):
            request.session['google_email'] = sociallogin.account.extra_data['email']
        
        # İsim bilgisi (ad + soyad)
        if sociallogin.account.extra_data.get('given_name'):
            request.session['google_first_name'] = sociallogin.account.extra_data['given_name']
        
        if sociallogin.account.extra_data.get('family_name'):
            request.session['google_last_name'] = sociallogin.account.extra_data['family_name']
        
        # Tam isim (fallback)
        if sociallogin.account.extra_data.get('name'):
            request.session['google_full_name'] = sociallogin.account.extra_data['name']
        
        # Google ID (kalıcı bağlantı için kritik)
        request.session['google_uid'] = sociallogin.account.uid
        request.session['google_provider'] = sociallogin.account.provider
        
        # Sosyal login nesnesinin kendisini de session'a kaydet
        # (Daha sonra kalıcı bağlantı kurmak için gerekli)
        request.session['pending_sociallogin'] = True
        
        # ONBOARDING MERKEZİNE YÖNLENDİR
        # Standart akışı durdur, kullanıcıyı özel sayfamıza gönder
        raise ImmediateHttpResponse(
            HttpResponseRedirect(reverse('google_onboarding_complete'))
        )
    
    def save_user(self, request, sociallogin, form=None):
        """
        Kullanıcı kaydı oluşturma sürecini override et.
        
        Not: pre_social_login'de yönlendirme yaptığımız için,
        yeni kullanıcılar için bu metod çağrılmayacak.
        Sadece güvenlik için override ediyoruz.
        """
        # Eğer buraya kadar geldiyse, onboarding'den gelmiş olmalı
        # Standart save işlemini yap
        return super().save_user(request, sociallogin, form)

