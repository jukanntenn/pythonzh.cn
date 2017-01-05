from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    date_hierarchy = 'created'
    list_display = ('title', 'created', 'modified', 'views', 'pinned', 'category', 'author', 'is_visible')

    def is_visible(self, obj):
        return not obj.is_removed

    is_visible.short_description = _('is visible')
    is_visible.boolean = True
