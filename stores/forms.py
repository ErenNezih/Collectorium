from django import forms
from .models import StorePolicy
from core import DEFAULT_FEATURE_FLAGS
import os
from messaging.contact_guard import redact_text


def _ff(name: str) -> bool:
    default = DEFAULT_FEATURE_FLAGS.get(name, False)
    raw = os.environ.get(name)
    return default if raw is None else raw.lower() in ("1", "true", "yes")


class StorePolicyForm(forms.ModelForm):
    class Meta:
        model = StorePolicy
        fields = [
            'return_policy_text',
            'shipping_policy_text',
            'contact_hours',
            'handling_time_days',
            'extra_notes',
        ]
        widgets = {
            'return_policy_text': forms.Textarea(attrs={'rows': 4}),
            'shipping_policy_text': forms.Textarea(attrs={'rows': 4}),
            'extra_notes': forms.Textarea(attrs={'rows': 3}),
        }

    def clean(self):
        cleaned = super().clean()
        strict = _ff('STRICT_CONTACT_GUARD')
        # Redact contact info from policy texts
        for field in ['return_policy_text', 'shipping_policy_text', 'extra_notes']:
            text = cleaned.get(field)
            if text:
                redacted, has_violation = redact_text(text, strict=strict)
                cleaned[field] = redacted
                if has_violation:
                    # Add non-fatal warning through form-level error
                    self.add_error(field, 'İletişim bilgileri tespit edildi ve redakte edildi.')
        return cleaned


