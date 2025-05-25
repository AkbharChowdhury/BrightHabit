from PIL.Image import Image
from ckeditor.fields import RichTextField
from django.core.files.storage import default_storage
from django.db import models
# from django.contrib.auth.models import User
from django.conf import settings
# from django.contrib.auth import get_user_model
from django.contrib.auth import get_user_model

import PIL


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(default='profile_pics/default.jpg', upload_to='profile_pics')
    bio = RichTextField(blank=True, null=True)

    def __str__(self):
        return f'{get_user_model().username} Profile'

    @property
    def full_name(self):
        return f'{get_user_model().first_name} {get_user_model().last_name}'.title()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if default_storage.exists(f'profile_pics/{self.image}'):
            with PIL.Image.open(fp=self.image.path) as image:
                if image.height > 300 or image.width > 300:
                    output_size = (300, 300)
                    image.thumbnail(output_size)
                    image.save(self.image.path)
