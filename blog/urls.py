from django.urls import path
from . import views


def name(title):
    return f'blog_{title}'


urlpatterns = [
    path('', views.index, name=name('index')),
    path('about/', views.about, name=name('about')),

]
