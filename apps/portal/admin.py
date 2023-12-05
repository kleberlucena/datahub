from django.contrib import admin
from django.utils.html import format_html


from apps.portal import models


admin.site.register(models.Gender)
admin.site.register(models.OrganizationalHierarchy)
admin.site.register(models.Enjoyer)

@admin.register(models.Military)
class MilitaryAdmin(admin.ModelAdmin):
    list_display = ('uuid_portal', 'register', 'rank', 'name', 'entity', 'active', 'image', 'foto_preview')
    search_fields = ('name', 'register')
    
    def foto_preview(self, obj):
        try:
            return format_html(
            f"<img src='{obj.image.url}' width='120' height='120' />")
        except:
            return format_html(
            f"<div width='120' height='120' ></div>")

@admin.register(models.Entity)
class EntityAdmin(admin.ModelAdmin):
    search_fields = ('name', 'active', 'id')
