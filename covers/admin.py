from django.contrib import admin
from .models import Cover


@admin.register(Cover)
class CoverAdmin(admin.ModelAdmin):
    list_display = ('cover', 'cover_thumbnail', 'caption')
