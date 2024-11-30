from django.contrib.auth.models import User
from django.utils import timezone
from django.db import models
from django.urls import reverse
from ckeditor.fields import RichTextField
from .my_helper import MyHelper


class ContactEmail(models.Model):
    email = models.EmailField(max_length=100)
    subject = models.CharField(max_length=200)
    message = models.TextField()


class Tag(models.Model):
    name = models.CharField(max_length=100)
    colour = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=100)
    body = RichTextField()
    post_snippet = models.CharField(max_length=100, blank=True, null=True)
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True, upload_to='images/')
    tags = models.ManyToManyField(Tag, blank=True, related_name='tags')
    search_fields = ('title', 'body', 'author')
    likes = models.ManyToManyField(User, related_name='post_likes', blank=True)

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog_detail', kwargs={'pk': self.pk})

    @property
    def get_content(self):
        return MyHelper.clean_text(self.body)

    @property
    def snippet(self):
        if self.post_snippet:
            return f'{MyHelper.clean_text(self.post_snippet[:100])}...'
        return f'{MyHelper.clean_text(self.body[:200])}...'
