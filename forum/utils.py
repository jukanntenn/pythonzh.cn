import re
import bleach
import markdown

from markdown.extensions.toc import TocExtension

from django.utils.text import slugify

from users.models import User

BLEACH_ALLOWED_TAGS = ['p', 'pre', 'blockquote', 'ol', 'ul', 'li', 'dl', 'dt', 'dd', 'figure', 'figcaption', 'hr', 'a',
                       'em', 'strong', 'cite', 'q', 'dfn', 'abbr', 'time', 'code', 'br', 'i', 'b', 'u', 's', 'sub',
                       'sup',
                       'ins', 'del', 'img', 'table', 'tr', 'td', 'th', 'caption', 'tbody', 'thead', 'tfoot', 'colgroup',
                       'col',
                       'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'acronym', 'span']

BLEACH_ALLOWED_ATTRIBUTES = {
    'a': ['href', 'title'],
    'abbr': ['title'],
    'acronym': ['title'],
    'span': ['class'],
    '*': ['id'],
    'img': ['src'],
}

MARKDOWN_EXTENSIONS = [
    'markdown.extensions.fenced_code',
    'markdown.extensions.tables',
    'markdown.extensions.codehilite',
    TocExtension(slugify=slugify),
]

MARKDOWN_EXTENSION_CONFIGS = {}


def bleach_value(value, tags=BLEACH_ALLOWED_TAGS, attributes=BLEACH_ALLOWED_ATTRIBUTES):
    return bleach.clean(value, tags=tags, attributes=attributes)


def markdown_value(value, extensions=MARKDOWN_EXTENSIONS,
                   extension_configs=MARKDOWN_EXTENSION_CONFIGS, *args, **kwargs):
    return markdown.markdown(value, extensions=extensions, extension_configs=extension_configs, *args, **kwargs)


def _pk_to_nickname(mo):
    pk = mo.group(1)
    user = User.objects.get(pk=pk)
    return '@[%s](' % user.nickname


def parse_nicknames(value):
    return re.sub(r'@\[([0-9]+)\]\(', _pk_to_nickname, value)
