from django.urls import path
from .views import PostDetailView, PostListView, about, PostCreateView


def name(title):
    return f'blog_{title}'


urlpatterns = [
    path('', PostListView.as_view(), name=name('index')),
    path('post/<int:pk>', PostDetailView.as_view(), name=name('detail')),
    path('about/', about, name=name('about')),
    path('post/new', PostCreateView.as_view(), name=name('create')),

]
