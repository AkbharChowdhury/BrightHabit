from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm


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
    template_name = 'users/profile.html'
    if not request.method == 'POST':
        context = {
            'user_form': UserUpdateForm(instance=request.user),
            'profile_form': ProfileUpdateForm(instance=request.user.profile)
        }
        return render(request, template_name, context)

    if request.method == 'POST':
        context = {
            'user_form': UserUpdateForm(request.POST, instance=request.user),
            'profile_form': ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        }
        if context['user_form'].is_valid() and context['profile_form'].is_valid():
            context['user_form'].save()
            context['profile_form'].save()
            messages.success(request, f'Your profile has been updated!')
            # return redirect(reverse_lazy('profile'))
            return redirect('profile')

        # return render(request, template_name, context)
