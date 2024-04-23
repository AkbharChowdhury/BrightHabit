from django.shortcuts import render

from blog.models import Post

posts = [
    {
        'author': 'John Doe',
        'title': 'first post!',
        'content': 'Beautiful day!',
        'date_posted': 'August 2,2018',
    },
    {
        'author': 'Jane Doe',
        'title': 'second post!',
        'content': 'Beautiful day 2!',
        'date_posted': 'August 28,2018',
    },
]


def index(request):
    context = {
        'posts': posts
    }
    return render(request, 'blog/index.html', {'posts': Post.objects.all()})


def about(request):
    return render(request, 'blog/about.html')
