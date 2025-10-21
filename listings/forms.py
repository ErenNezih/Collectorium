from django import forms
from .models import Listing, ListingImage


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class ImageUploadForm(forms.ModelForm):
    images = forms.ImageField(
        widget=MultipleFileInput(attrs={'multiple': True}),
        required=False,
        label="İlan Resimleri (Birden fazla seçebilirsiniz)"
    )

    class Meta:
        model = ListingImage
        fields = ['images']

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = [
            'product', 'title', 'description', 'price', 
            'condition', 'stock'
        ]
        widgets = {
            'product': forms.Select(attrs={'class': 'form-select'}),
            'title': forms.TextInput(attrs={'placeholder': 'Örn: Pokémon Charizard VMAX Kartı'}),
            'description': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Ürününüzle ilgili tüm detayları alıcıyla paylaşın.'}),
            'price': forms.NumberInput(attrs={'placeholder': 'Örn: 250.00'}),
            'condition': forms.Select(),
            'stock': forms.NumberInput(attrs={'min': '1', 'value': '1'}),
        }
        labels = {
            'product': 'İlgili Katalog Ürünü',
            'title': 'İlan Başlığı',
            'description': 'Açıklama',
            'price': 'Fiyat (₺)',
            'condition': 'Ürünün Durumu',
            'stock': 'Stok Adedi',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Tailwind CSS sınıflarını tüm form alanlarına dinamik olarak ekle
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'w-full px-4 py-2 mt-2 border rounded-md focus:outline-none focus:ring-1 focus:ring-brand-red'
            })










