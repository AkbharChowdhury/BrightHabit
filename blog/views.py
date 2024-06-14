from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.models import User
from blog.models import Post

from django.db.models import Q


class PostListView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

    #     search functionality: https://medium.com/@j.yanming/simple-search-page-with-pagination-in-django-154ad259f4d7

    def get_queryset(self):
        search = dict(title=self.request.GET.get('title'), author=self.request.GET.get('author'))
        if any(search.values()): return self.search_filter(**search)
        return self.model.objects.all()

    def __full_text_search(self, title: str):
        return Q(title__icontains=title) | Q(body__icontains=title)

    def __author_search(self, author: str):
        return Q(author=author)

    def search_filter(self, title: str, author: str):
        article_filter = self.model.objects.filter

        if title is not None and author is not None:
            return article_filter(
                self.__author_search(author) &
                self.__full_text_search(title)
            )

        if title is not None:
            return article_filter(self.__full_text_search(title))
        if author is not None:
            return self.__author_search(author)


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    # ordering = ['-date_posted']
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return self.model.objects.filter(author=user).order_by('-date_posted')

    # def get_context_data(self, *args, **kwargs):
    #     context = super(self.__class__, self).get_context_data(*args, **kwargs)
    #     context['author_name'] = 'hello'


class PostDetailView(DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'blog/detail.html'


class PostCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Post
    context_object_name = 'post'
    template_name = 'blog/create.html'
    fields = ['title', 'body', 'image']
    success_message = f'blog created'.title()

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    context_object_name = 'post'
    template_name = 'blog/update.html'
    fields = ['title', 'body', 'image']

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
