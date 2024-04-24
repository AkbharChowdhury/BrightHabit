from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import View, CreateView

from .forms import UserRegisterForm
from django.contrib.auth.decorators import login_required


class RegisterView(CreateView):
    form_class = UserRegisterForm
    template_name = 'users/register.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {"form": self.form_class})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}. you can now login')
            return redirect(reverse_lazy('login'))

        return render(request, 'users/register.html', {'form': form})



# def register(request):
#     form = UserRegisterForm(request.POST) if request.method == 'POST' else UserRegisterForm()
#     if request.method == 'POST':
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data.get('username')
#             messages.success(request, f'Account created for {username}. you can now login')
#             return redirect('login')
#
#     return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    return render(request, 'users/profile.html')
