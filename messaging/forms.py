from django import forms
from .models import Message, Conversation


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Mesajınızı yazın...'
            })
        }


class ConversationForm(forms.ModelForm):
    class Meta:
        model = Conversation
        fields = ['subject']
        widgets = {
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Konu (İsteğe bağlı)'
            })
        }











