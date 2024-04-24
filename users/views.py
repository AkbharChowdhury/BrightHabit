from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import UserRegisterForm


def register(request):
    form = UserRegisterForm(request.POST) if request.method == 'POST' else UserRegisterForm()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}. you can now login')
            return redirect('login')

    return render(request, 'users/register.html', {'form': form})
