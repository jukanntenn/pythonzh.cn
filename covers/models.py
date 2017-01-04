from django.db import models
from django.utils.translation import ugettext_lazy as _

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from model_utils.models import TimeStampedModel


class Cover(TimeStampedModel):
    cover = models.ImageField(_('cover'), upload_to='covers/%Y/%m/%d/')
    caption = models.CharField(_('caption'), max_length=255, blank=True)
    cover_thumbnail = ImageSpecField(source='cover',
                                     processors=[ResizeToFill(146, 146)],
                                     format='JPEG',
                                     options={'quality': 80})

    def __str__(self):
        return self.cover

    class Meta:
        verbose_name = 'cover'
        verbose_name_plural = 'covers'
