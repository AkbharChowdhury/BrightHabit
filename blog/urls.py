from django.urls import path
from .views import (
    PostDetailView,
    PostListView,
    about,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView
)


def name(title):
    return f'blog_{title}'


urlpatterns = [
    path('', PostListView.as_view(), name=name('index')),
    path('user/<str:username>', UserPostListView.as_view(), name=name('user_posts')),
    path('post/<int:pk>', PostDetailView.as_view(), name=name('detail')),
    path('post/new', PostCreateView.as_view(), name=name('create')),
    path('post/<int:pk>/update', PostUpdateView.as_view(), name=name('update')),
    path('post/<int:pk>/delete', PostDeleteView.as_view(), name=name('delete')),

    path('about/', about, name=name('about')),

]
