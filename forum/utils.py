import re
import bleach
import markdown

from django.conf import settings
from django.contrib.contenttypes.models import ContentType

from users.models import User

bleach_args = {}
possible_settings = {
    'BLEACH_ALLOWED_TAGS': 'tags',
    'BLEACH_ALLOWED_ATTRIBUTES': 'attributes',
    'BLEACH_ALLOWED_STYLES': 'styles',
    'BLEACH_STRIP_TAGS': 'strip',
    'BLEACH_STRIP_COMMENTS': 'strip_comments',
}

markdown_extensions = settings.MARKDOWN_EXTENSIONS
markdown_extension_configs = settings.MARKDOWN_EXTENSION_CONFIGS

for setting, kwarg in possible_settings.items():
    if hasattr(settings, setting):
        bleach_args[kwarg] = getattr(settings, setting)


def _pk_to_nickname(mo):
    pk = mo.group(1)
    user = User.objects.get(pk=pk)
    return '@[%s](' % user.nickname


def parse_nicknames(value):
    return re.sub(r'@\[([0-9]+)\]\(', _pk_to_nickname, value)


def mark(value, extensions=markdown_extensions, extension_configs=markdown_extension_configs,
         *args, **kwargs):
    return markdown.markdown(value, extensions=extensions, extension_configs=extension_configs, *args, **kwargs)


def bleach_value(value):
    return bleach.clean(value, **bleach_args)


def get_ctype_pk(obj):
    return ContentType.objects.get_for_model(obj).pk
