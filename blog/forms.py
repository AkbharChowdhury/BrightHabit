from django import forms
from .models import ContactEmail


class ContactEmailForm(forms.ModelForm):
    class Meta:
        model = ContactEmail
        fields = ('email', 'subject', 'message')
