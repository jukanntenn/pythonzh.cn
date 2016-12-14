import os

from django.db import models
from django.core.files.base import ContentFile
from django.contrib.auth.models import AbstractUser
from django.core import urlresolvers

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

from .mugshot import Avatar


def user_mugshot_path(instance, filename):
    return os.path.join('mugshots', instance.username, filename)


class User(AbstractUser):
    last_login_ip = models.GenericIPAddressField(unpack_ipv4=True, blank=True, null=True)
    ip_joined = models.GenericIPAddressField(unpack_ipv4=True, blank=True, null=True)

    nickname = models.CharField(max_length=50, unique=True)
    signature = models.CharField(max_length=100, blank=True)
    mugshot = models.ImageField(upload_to=user_mugshot_path)
    mugshot_thumbnail = ImageSpecField(source='mugshot',
                                       processors=[ResizeToFill(96, 96)],
                                       format='JPEG',
                                       options={'quality': 80})

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if not self.nickname:
            self.nickname = self.username

        if not self.mugshot:
            print('I involked')
            avatar = Avatar(rows=10, columns=10)
            image_byte_array = avatar.get_image(string=self.username,
                                                width=480,
                                                height=480,
                                                pad=10)
            self.mugshot.save('default_mugshot.png', ContentFile(image_byte_array), save=False)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return urlresolvers.reverse('users:detail', args=(self.username,))
