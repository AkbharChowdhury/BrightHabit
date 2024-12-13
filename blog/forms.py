from django import forms
from .models import ContactEmail, Post, Tag


class ContactEmailForm(forms.ModelForm):
    class Meta:
        model = ContactEmail
        fields = ('email', 'subject', 'message')


class PostForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple(), queryset=Tag.objects.all())
    class Meta:
        model = Post
        fields = ('title', 'body', 'image', 'tags', 'post_snippet')
