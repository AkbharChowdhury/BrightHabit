from django.urls import path
from .views import PostDetailView, PostListView, about, PostCreateView, PostUpdateView


def name(title):
    return f'blog_{title}'


urlpatterns = [
    path('', PostListView.as_view(), name=name('index')),
    path('post/<int:pk>', PostDetailView.as_view(), name=name('detail')),
    path('post/new', PostCreateView.as_view(), name=name('create')),
    path('post/<int:pk>/update', PostUpdateView.as_view(), name=name('update')),
    path('about/', about, name=name('about')),

]
