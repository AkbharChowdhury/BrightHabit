from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from autofocus import Autofocus
from .custom_validation import CustomValidation
from .models import Profile


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
        if CustomValidation.email_exists(email):
            raise ValidationError("A user with this email already exists!")
        return email


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    username = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    class Meta:
        model = User
        fields = ('username', 'email')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if self.email_exists(email=email, excluded_email='john@gmail.com'):
            raise forms.ValidationError("A user with this email is registered.")
        return email

    def email_exists(self, email: str, excluded_email: str):
        return User.objects.filter(email=email).exclude(email=excluded_email).exists()


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']
