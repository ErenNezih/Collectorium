from django import forms
from catalog.models import Category
from listings.models import Listing


class SearchForm(forms.Form):
    query = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ürün, kategori veya mağaza ara...'
        })
    )
    
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        empty_label="Tüm Kategoriler",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    condition = forms.ChoiceField(
        choices=Listing.CONDITION_CHOICES,
        required=False,
        empty_label="Tüm Durumlar",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    min_price = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Min Fiyat',
            'step': '0.01'
        })
    )
    
    max_price = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Max Fiyat',
            'step': '0.01'
        })
    )
    
    sort_by = forms.ChoiceField(
        choices=[
            ('newest', 'En Yeni'),
            ('oldest', 'En Eski'),
            ('price_low', 'Fiyat (Düşük)'),
            ('price_high', 'Fiyat (Yüksek)'),
            ('title_asc', 'Başlık (A-Z)'),
            ('title_desc', 'Başlık (Z-A)'),
        ],
        initial='newest',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    view_type = forms.ChoiceField(
        choices=[
            ('grid', 'Grid Görünüm'),
            ('list', 'Liste Görünüm'),
        ],
        initial='grid',
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'})
    )





