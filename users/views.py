from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm


class RegisterView(CreateView):
    form_class = UserRegisterForm
    template_name = 'users/register.html'

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}. you can now login')
            return redirect(reverse_lazy('login'))
        return render(request, self.template_name, {'form': form})


class Profile(LoginRequiredMixin, CreateView):
    template_name = 'users/profile.html'
    user_form = 'user_form'
    profile_form = 'profile_form'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {
            self.user_form: UserUpdateForm(instance=request.user),
            self.profile_form: ProfileUpdateForm(instance=request.user.profile)
        })

    def post(self, request, *args, **kwargs):
        user_form = self.user_form
        profile_fom = self.profile_form
        context = dict(
            user_form=UserUpdateForm(request.POST, instance=request.user),
            profile_form=ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        )

        if context[user_form].is_valid() and context[profile_fom].is_valid():
            context[user_form].save()
            context[profile_fom].save()
            messages.success(request, 'your profile has been updated!'.capitalize())
            return redirect('profile')
        messages.error(request, "Whoops, something went wrong.")
        return render(request, self.template_name, context)
