from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from BrightHabit.settings import ADMIN_EMAIL
from .author import Author
from .custom_tags import CustomTagsMixin
from .forms import ContactEmailForm
from .forms import PostForm
from .http_request import HttpRequest
from .models import Post, ContactEmail
from .my_helper import MyHelper
from .params import Params
from .search_posts import SearchPosts

TAG_COLOUR = CustomTagsMixin.tag_colour()


class PostListView(ListView, CustomTagsMixin):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    ordering = '-date_posted'
    paginate_by = SearchPosts.records_per_page()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(Params(self.request).get_context_data())
        return context

    def get_queryset(self):
        search = dict(title=self.request.GET.get('title'), tags=self.request.GET.getlist('tags'))
        if any(search.values()):
            return SearchPosts(**search).search().order_by(self.ordering)
        return self.model.objects.all().order_by(self.ordering)


class UserPostListView(ListView, CustomTagsMixin):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = SearchPosts.records_per_page()
    ordering = '-date_posted'

    def get_queryset(self):
        title = self.request.GET.get('title')
        tags = self.request.GET.getlist('tags')
        author = Q(author=Author.get_author_by_username(self.kwargs.get('username')))
        tags_search = SearchPosts.tags_search(tags) if tags and MyHelper.list_is_not_empty(tags) else Q()
        return self.model.objects.filter(tags_search & author & SearchPosts.full_text_search(title)).order_by(
            self.ordering)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(Params(self.request).get_context_data())
        return context


class PostDetailView(DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'blog/detail.html'

    def user(self) -> User:
        return self.request.user

    def post(self, request, *args, **kwargs):
        http_request = HttpRequest(self.request)
        if http_request.is_http_request():
            self.toggle_like(post_id=http_request.get_post_id('post_id'), user=self.user())
            return JsonResponse(self.like_data())

    def toggle_like(self, post_id: str, user: User) -> None:
        post = get_object_or_404(self.model, id=int(post_id))
        post.likes.remove(user) if post.likes.filter(id=user.id).exists() else post.likes.add(user)

    def like_data(self, context: dict[str, str | int] = None):
        if context is None:
            context = {}
        post_likes = get_object_or_404(self.model, id=self.kwargs['pk'])
        liked = False if post_likes.likes.filter(id=self.user().id).exists() else True
        context['total_likes'] = post_likes.total_likes()
        context['liked_icon'] = 'fa-regular' if liked else 'fa-solid'
        context['liked'] = liked
        return context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag_colour'] = TAG_COLOUR
        context['default_profile_pic'] = 'https://static.vecteezy.com/system/resources/thumbnails/009/292/244/small/default-avatar-icon-of-social-media-user-vector.jpg'
        context.update(self.like_data(context=context))
        return context


class PostCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Post
    context_object_name = 'post'
    template_name = 'blog/create.html'
    form_class = PostForm
    success_message = f'blog created'.title()

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostBelongsToUserMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


class PostUpdateView(PostBelongsToUserMixin, UpdateView):
    model = Post
    context_object_name = 'post'
    template_name = 'blog/update.html'
    form_class = PostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostDeleteView(PostBelongsToUserMixin, DeleteView):
    model = Post
    context_object_name = 'post'
    template_name = 'blog/delete.html'
    success_url = '/'
    success_message = f'blog deleted'.title()


def about(request):
    return render(request, 'blog/about.html')


class ContactView(CreateView):
    model = ContactEmail
    template_name = 'emails/contact.html'
    form_class = ContactEmailForm

    def get_data(self, param: str):
        return self.request.POST.get(param)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            if send_mail(subject=self.get_data('subject'), message=self.get_data('message'),
                         from_email=self.get_data('email'), recipient_list=[ADMIN_EMAIL],
                         fail_silently=False):
                messages.success(request, "Your enquiry has been sent!")
                return redirect(reverse_lazy('blog_contact'))
        messages.error(request, MyHelper.error_message())
        return render(request, self.template_name, {'form': form})
