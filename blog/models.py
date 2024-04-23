from django.contrib.auth.models import User
from django.utils import timezone
from django.db import models
from ckeditor.fields import RichTextField
from django.utils.safestring import mark_safe


class Post(models.Model):
    title = models.CharField(max_length=100)
    body = RichTextField(blank=True, null=True)
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True, upload_to='images/')

    def __str__(self):
        return self.title

    @property
    def snippet(self):
        return mark_safe(f'{self.body
                         .removeprefix('<pre>')
                         .removesuffix('</pre>')
                            [:200]}...')

