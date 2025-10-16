"""
Collectorium Forms
'Keystone' Operasyonu - Google Onboarding Form
"""

from django import forms
from .models import Address, VerifiedSeller, VerifiedSellerDocument


class GoogleOnboardingForm(forms.Form):
    """
    Google ile giriş yapan yeni kullanıcılar için onboarding formu.
    
    Bu form, Google'dan gelen temel bilgilere ek olarak:
    - Kullanıcı adı
    - Telefon numarası
    - Adres bilgileri
    toplar.
    """
    
    # Kullanıcı Bilgileri
    username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'auth-input w-full px-4 py-3 rounded-xl',
            'placeholder': 'Kullanıcı adınızı seçin'
        }),
        label='Kullanıcı Adı',
        help_text='Platformda görünecek adınız'
    )
    
    phone = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'auth-input w-full px-4 py-3 rounded-xl',
            'placeholder': '+90 5XX XXX XX XX',
            'id': 'id_phone'
        }),
        label='Telefon Numarası'
    )
    
    # Adres Bilgileri
    address_title = forms.CharField(
        max_length=100,
        initial='Ev',
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'auth-input w-full px-4 py-3 rounded-xl',
            'placeholder': 'Ev, İş, vs.'
        }),
        label='Adres Başlığı'
    )
    
    city = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'auth-input w-full px-4 py-3 rounded-xl',
            'placeholder': 'İstanbul, Ankara, İzmir...'
        }),
        label='Şehir'
    )
    
    district = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'auth-input w-full px-4 py-3 rounded-xl',
            'placeholder': 'İlçe'
        }),
        label='İlçe'
    )
    
    full_address = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={
            'class': 'auth-input w-full px-4 py-3 rounded-xl',
            'placeholder': 'Mahalle, sokak, bina no, daire no...',
            'rows': 3
        }),
        label='Açık Adres'
    )
    
    postal_code = forms.CharField(
        max_length=10,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'auth-input w-full px-4 py-3 rounded-xl',
            'placeholder': 'Posta Kodu (opsiyonel)'
        }),
        label='Posta Kodu'
    )
    
    # Hesap Türü (Buyer/Seller)
    role = forms.ChoiceField(
        choices=[('buyer', 'Alıcı'), ('seller', 'Satıcı')],
        initial='buyer',
        required=True,
        widget=forms.RadioSelect(),
        label='Hesap Türü'
    )
    
    # Telefon onayı simülasyonu için hidden field
    phone_verified = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.HiddenInput()
    )
    
    def clean_username(self):
        """Kullanıcı adının benzersiz olduğundan emin ol"""
        from .models import User
        username = self.cleaned_data['username']
        
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(
                'Bu kullanıcı adı zaten kullanımda. Lütfen başka bir tane seçin.'
            )
        
        return username
    
    def clean_phone(self):
        """Telefon numarasını temizle ve formatla"""
        phone = self.cleaned_data['phone']
        
        # Basit validasyon - en az 10 karakter
        phone = phone.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')
        
        if len(phone) < 10:
            raise forms.ValidationError(
                'Geçerli bir telefon numarası girin.'
            )
        
        return phone
    
    def clean(self):
        """Telefon onayının yapıldığından emin ol"""
        cleaned_data = super().clean()
        phone_verified = cleaned_data.get('phone_verified')
        
        if not phone_verified:
            raise forms.ValidationError(
                'Lütfen telefon numaranızı onaylayın.'
            )
        
        return cleaned_data


class VerifiedSellerApplicationForm(forms.ModelForm):
    documents = forms.FileField(widget=forms.ClearableFileInput(attrs={"multiple": True}), required=True, help_text="Kimlik/şirket belgeleri")

    class Meta:
        model = VerifiedSeller
        fields = ["company_name", "tax_no"]

    def save(self, user, commit=True):
        verified, _ = VerifiedSeller.objects.get_or_create(user=user, defaults={
            "company_name": self.cleaned_data.get("company_name", ""),
            "tax_no": self.cleaned_data.get("tax_no", ""),
            "status": "pending",
        })
        # update details in case of resubmission
        verified.company_name = self.cleaned_data.get("company_name", "")
        verified.tax_no = self.cleaned_data.get("tax_no", "")
        if commit:
            verified.save()
        files = self.files.getlist('documents')
        for f in files:
            VerifiedSellerDocument.objects.create(verified_seller=verified, file=f)
        return verified
