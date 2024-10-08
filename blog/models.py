from django.contrib.auth.models import User
from django.utils import timezone
from django.db import models
from django.utils.safestring import mark_safe
from ckeditor.fields import RichTextField
from django.urls import reverse


class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=100)
    body = RichTextField(blank=True, null=True)
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True, upload_to='images/')
    tags = models.ManyToManyField(Tag, blank=True, related_name='tags')

    search_fields = ('title', 'body', 'author')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog_detail', kwargs={'pk': self.pk})

    @property
    def get_content(self):
        return self.__clean_text(self.body)

    @property
    def snippet(self):
        return f'{self.__clean_text(self.body[:200])}...'

    def __clean_text(self, text):
        return mark_safe(text
                         .removeprefix('<pre>')
                         .removesuffix('</pre>'))
