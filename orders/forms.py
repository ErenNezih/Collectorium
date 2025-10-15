from django import forms
from accounts.models import Address

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['address_title', 'full_address', 'district', 'city', 'country']
        labels = {
            'address_title': 'Adres Başlığı (Örn: Ev Adresim)',
            'full_address': 'Açık Adres',
            'district': 'İlçe / Semt',
            'city': 'Şehir',
            'country': 'Ülke',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'w-full px-4 py-2 mt-2 border rounded-md focus:outline-none focus:ring-1 focus:ring-brand-red'
            })


class AddressSelectionForm(forms.Form):
    selected_address = forms.ModelChoiceField(
        queryset=None,
        widget=forms.RadioSelect,
        empty_label=None,
        required=True
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields['selected_address'].queryset = Address.objects.filter(user=self.user)





