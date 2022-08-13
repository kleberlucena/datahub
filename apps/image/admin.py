from django.contrib import admin
from guardian.admin import GuardedModelAdmin
from django.utils.html import format_html

from .models import Image


@admin.register(Image)
class ImageAdmin(GuardedModelAdmin):
    list_display = ('uuid', 'created_by', 'foto_preview', 'created_at', 'updated_at')
    readonly_fields = ['foto_preview']

    def foto_preview(self, obj):
        return format_html(
            f"<img src='{obj}' width='120' height='120' style='border-radius: 50% 50%;'/>")