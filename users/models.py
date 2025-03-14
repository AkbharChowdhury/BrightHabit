from PIL.Image import Image
from ckeditor.fields import RichTextField
from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='profile_pics/default.jpg', upload_to='profile_pics')
    bio = RichTextField(blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} Profile'

    @property
    def full_name(self):
        return f'{self.user.first_name} {self.user.last_name}'.title()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        image = Image.open(self.image)
        if image.height > 300 or image.width > 300:
            output_size = (300, 300)
            image.thumbnail(output_size)
            image.save(self.image.path)
