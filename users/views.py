from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.files.storage import default_storage
from django.db.models import Count
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

import users.models
from blog.models import Post, Tag
from blog.my_helper import MyHelper
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm


class RegisterView(CreateView):
    form_class = UserRegisterForm
    template_name = 'users/register.html'

    def get_success_url(self):
        return redirect(reverse_lazy('login'))

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Account created for {form.cleaned_data.get('username')}. you can now login')
            return self.get_success_url()
        return render(request, self.template_name, {'form': form})


class Profile(LoginRequiredMixin, CreateView):
    template_name = 'users/profile.html'
    user_form = 'user_form'
    profile_form = 'profile_form'

    def get_user_form(self, request):
        request_method = None if request.method == 'GET' else self.request.POST
        return UserUpdateForm(request_method, instance=request.user, current_user=request.user)

    def get(self, request, *args, **kwargs):
        user: User = request.user
        user_profile_image = users.models.Profile().image
        user_last_post = Post.objects.filter(author=user).order_by('-date_posted')
        num_posts = Post.objects.filter(author=user).count()
        post_tags = Tag.objects.all().filter(tags__author__email=user.email).annotate(count=Count('tags'))

        return render(request, self.template_name, {
            self.user_form: self.get_user_form(request),
            self.profile_form: ProfileUpdateForm(instance=user.profile),
            'num_posts': num_posts,
            'last_posted': user_last_post[0] if user_last_post.exists() else '',
            'plural': 's' if num_posts > 1 else '',
            'post_tags': post_tags,
            'user_profile_image': user_profile_image if default_storage.exists(f'profile_pics/{user_profile_image}') else 'empty'
        })

    def post(self, request, *args, **kwargs):
        user_form = self.user_form
        profile_fom = self.profile_form
        context = dict(
            user_form=self.get_user_form(request),
            profile_form=ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        )

        if not context[user_form].is_valid() and context[profile_fom].is_valid():
            messages.error(request, MyHelper.error_message())
            return render(request, self.template_name, context)

        context[user_form].save()
        context[profile_fom].save()
        messages.success(request, 'your profile has been updated!'.capitalize())
        return redirect('profile')
