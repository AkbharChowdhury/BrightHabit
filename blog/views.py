from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from blog.models import Post


# posts = [
#     {
#         'author': 'John Doe',
#         'title': 'first post!',
#         'content': 'Beautiful day!',
#         'date_posted': 'August 2,2018',
#     },
#     {
#         'author': 'Jane Doe',
#         'title': 'second post!',
#         'content': 'Beautiful day 2!',
#         'date_posted': 'August 28,2018',
#     },
# ]

class PostListView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']


class PostDetailView(DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'blog/detail.html'


class PostCreateView(CreateView):
    model = Post
    context_object_name = 'post'
    template_name = 'blog/create.html'
    fields = ['title', 'body', 'image']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)





def about(request):
    return render(request, 'blog/about.html')
