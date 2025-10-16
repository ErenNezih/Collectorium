from django import forms
from .models import Report


class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['reason', 'description']
        widgets = {
            'reason': forms.TextInput(attrs={'class': 'rounded border px-3 py-2'}),
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'rounded border px-3 py-2'}),
        }


