from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Profile


# from crispy_forms.helper import FormHelper
# from crispy_forms.layout import Layout, Submit, Field

class Autofocus:
    def __init__(self, fields):
        self.fields = fields

    def change_focus(self, old, new):
        self.fields[old].widget.attrs.update({'autofocus': ''})
        self.fields[new].widget.attrs.update({'autofocus': 'autofocus'})


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=200)
    last_name = forms.CharField(max_length=200)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        Autofocus(self.fields).change_focus(old='username', new='first_name')

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise ValidationError("A user with this email already exists!")
        return email


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('username', 'email')


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('image',)
