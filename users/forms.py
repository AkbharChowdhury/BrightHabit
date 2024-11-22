from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from autofocus import Autofocus
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
        if self.__email_exists(email):
            raise ValidationError("A user with this email already exists!")
        return email

    def __email_exists(self, email):
        return User.objects.filter(email=email).exists()


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    username = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    # def username_exists(username):
    #     return User.objects.filter(username=username).exists()

    class Meta:
        model = User
        fields = ('username', 'email')


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('image',)
