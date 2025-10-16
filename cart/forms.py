from django import forms

class CartAddListingForm(forms.Form):
    quantity = forms.IntegerField(
        min_value=1,
        initial=1,
        widget=forms.NumberInput(attrs={
            'class': 'w-20 text-center border-gray-300 focus:ring-brand-red focus:border-brand-red rounded-md',
            'min': '1'
        })
    )
    override = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)






