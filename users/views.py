from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Count
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from blog.author import Author
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from blog.models import Post, Tag
from django.db import connection


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

    def get_user_form(self, request):
        request_method = None if request.method == 'GET' else self.request.POST
        return UserUpdateForm(request_method, instance=request.user, current_user=request.user)

    def get(self, request, *args, **kwargs):
        user_last_post = Post.objects.filter(author=request.user).order_by('-date_posted')
        num_posts = Post.objects.filter(author=request.user).count()
        post_tags = Tag.objects.all().filter(tags__author__email=request.user.email).annotate(count=Count('tags'))
        return render(request, self.template_name, {
            self.user_form: self.get_user_form(request),
            self.profile_form: ProfileUpdateForm(instance=request.user.profile),
            'num_posts': num_posts,
            'last_posted': user_last_post[0] if user_last_post.exists() else '',
            'plural': 's' if num_posts > 1 else '',
            'post_tags': post_tags,
        })

    def post(self, request, *args, **kwargs):
        user_form = self.user_form
        profile_fom = self.profile_form
        context = dict(
            user_form=self.get_user_form(request),
            profile_form=ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        )
        if not context[user_form].is_valid() and context[profile_fom].is_valid():
            messages.error(request, "Whoops, something went wrong.")
            return render(request, self.template_name, context)

        context[user_form].save()
        context[profile_fom].save()
        messages.success(request, 'your profile has been updated!'.capitalize())
        return redirect('profile')
