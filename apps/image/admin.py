from django.contrib import admin

from .models import Image


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'created_by', 'created_at', 'updated_at')
