from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from blog.models import Post
from .search_posts import SearchPosts
from .author import Author


class PostListView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = SearchPosts.records_per_page()

    # def get_context_data(self, **kwargs):
    #     data = super().get_context_data(**kwargs)
    #     data['page_title'] = 'Authors'
    #     return data

    def get_queryset(self):
        search = dict(title=self.request.GET.get('title'), author=self.request.GET.get('author'))
        if any(search.values()):
            search = SearchPosts(**search)
            return search.search()
        return self.model.objects.all()


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    # ordering = ['-date_posted']
    paginate_by = SearchPosts.records_per_page()

    def get_queryset(self):
        user = Author.get_author(username=self.kwargs.get('username'))
        title = self.request.GET.get('title')
        if title is not None:
            return self.model.objects.filter(Q(author=user) & Q(title__icontains=title)).order_by('-date_posted')
        return self.model.objects.filter(author=user).order_by('-date_posted')


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
