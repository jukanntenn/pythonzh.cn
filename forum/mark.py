from django.conf import settings

import markdown


def markdownify(value, extensions=settings.MARKDOWN_EXTENSIONS, extension_configs=settings.MARKDOWN_EXTENSION_CONFIGS,
                *args, **kwargs):
    return markdown.markdown(value, extensions=extensions, extension_configs=extension_configs, *args, **kwargs)
