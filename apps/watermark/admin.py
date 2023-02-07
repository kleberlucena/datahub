from django.contrib import admin

from . import models


@admin.register(models.TemporaryURL)
class TemporaryURLAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'temporary_url', 'expiration_date')


@admin.register(models.UserMark)
class UserMarkAdmin(admin.ModelAdmin):
    list_display = ('user', 'uuid', 'mark_text', 'created_at', 'updated_at', 'active')
    

@admin.register(models.MarkTemplates)
class MarkTemplatesAdmin(admin.ModelAdmin):
    list_display = ('uuid_user_mark', 'mark_128', 'mark_480', 'mark_720')