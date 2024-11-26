from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.base import ContextMixin

from BrightHabit.settings import APP_NAME, ADMIN_EMAIL
from blog.models import Post, Tag, ContactEmail
from .author import Author
from .forms import ContactEmailForm
from .httprequest import HttpRequest
from .my_helper import MyHelper
from .search_posts import SearchPosts

TAG_COLOUR = 'secondary'


class CustomTags(ContextMixin):
    MIN_NUM_TAGS = 3

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.kwargs.get('username'):
            author_username = Q(author=Author.get_author_by_username(username=self.kwargs.get('username')))
            context['tags'] = Tag.objects.filter(Q(tags__in=Post.objects.filter(author_username))).distinct()
            return context
        tags = Tag.objects.filter(
            Q(tags__in=Post.objects.all())).distinct() if 'show_all_tags' in self.request.GET else Tag.objects.filter(
            Q(tags__in=Post.objects.all())).distinct()[:self.MIN_NUM_TAGS]
        context['tags'] = tags
        return context


class PostListView(ListView, CustomTags):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    ordering = '-date_posted'
    paginate_by = SearchPosts.records_per_page()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['app_name'] = APP_NAME
        context['selected_tags'] = self.request.GET.getlist('tags')
        context['tag_colour'] = TAG_COLOUR
        return context

    def get_queryset(self):
        search = dict(title=self.request.GET.get('title'), tags=self.request.GET.getlist('tags'))
        if any(search.values()):
            return SearchPosts(**search).search().order_by(self.ordering)
        return self.model.objects.all().order_by(self.ordering)


class UserPostListView(ListView, CustomTags):
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
        context['app_name'] = APP_NAME
        context['selected_tags'] = self.request.GET.getlist('tags')
        context['tag_colour'] = TAG_COLOUR
        return context


class PostDetailView(DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'blog/detail.html'

    def post(self, request, *args, **kwargs):
        http_request = HttpRequest(self.request)
        if http_request.is_http_request():
            self.toggle_like(http_request.get_post_id('post_id'))
            return JsonResponse(self.like_data())

    def toggle_like(self, post_id) -> None:
        post = get_object_or_404(self.model, id=post_id)
        post.likes.remove(self.request.user) if post.likes.filter(
            id=self.request.user.id).exists() else post.likes.add(
            self.request.user)

    def like_data(self, context=None):
        if context is None:
            context = {}
        post_likes = get_object_or_404(self.model, id=self.kwargs['pk'])
        liked = False if post_likes.likes.filter(id=self.request.user.id).exists() else True
        context['total_likes'] = post_likes.total_likes()
        context['liked_icon'] = 'fa-regular' if liked else 'fa-solid'
        context['liked'] = liked
        return context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag_colour'] = TAG_COLOUR
        context.update(self.like_data(context=context))
        self.like_data(context)
        return context


class PostCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Post
    context_object_name = 'post'
    template_name = 'blog/create.html'
    fields = ('title', 'body', 'image', 'tags', 'post_snippet')
    success_message = f'blog created'.title()

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    context_object_name = 'post'
    template_name = 'blog/update.html'
    fields = ('title', 'body', 'image', 'tags', 'post_snippet')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    context_object_name = 'post'
    template_name = 'blog/delete.html'
    success_url = '/'
    success_message = f'blog deleted'.title()

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


def about(request):
    return render(request, 'blog/about.html')


class ContactView(CreateView):
    model = ContactEmail
    template_name = 'emails/contact.html'
    form_class = ContactEmailForm

    def post(self, request, *args, **kwargs):
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        email = request.POST.get('email')
        form = self.form_class(request.POST)
        if form.is_valid():
            if send_mail(subject=subject, message=message, from_email=email, recipient_list=[ADMIN_EMAIL],
                         fail_silently=False):
                messages.success(request, "Your enquiry has been sent!")
                return redirect(reverse_lazy('blog_contact'))
        messages.error(request, "Please fill all the fields")
        return render(request, self.template_name, {'form': form})
