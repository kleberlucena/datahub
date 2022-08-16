from django.contrib import admin
from django.utils.html import format_html
from guardian.admin import GuardedModelAdmin
from safedelete.admin import SafeDeleteAdmin, SafeDeleteAdminFilter, highlight_deleted

from apps.person.models import *


@admin.register(Person)
class PersonAdmin(SafeDeleteAdmin, GuardedModelAdmin):
    list_display = (highlight_deleted, "highlight_deleted_field", 'uuid', 'created_at', 'updated_at',
                    "created_by", "deleted_by") + SafeDeleteAdmin.list_display
    list_filter = ("created_by", SafeDeleteAdminFilter,) + SafeDeleteAdmin.list_filter
    search_fields = ('uuid',)
    exclude = ()
    field_to_highlight = "id"


PersonAdmin.highlight_deleted_field.short_description = PersonAdmin.field_to_highlight


@admin.register(Face)
class FaceAdmin(SafeDeleteAdmin, GuardedModelAdmin):
    list_display = (highlight_deleted, "highlight_deleted_field", 'uuid', 'foto_preview', 'created_at',
                    'updated_at', "created_by", "deleted_by") + SafeDeleteAdmin.list_display
    list_filter = ("created_by", SafeDeleteAdminFilter,) + SafeDeleteAdmin.list_filter
    search_fields = ('uuid',)
    exclude = ()
    field_to_highlight = "id"

    def foto_preview(self, obj):
        try:
            return format_html(
            f"<img src='{obj.file.url}' width='120' height='120' style='border-radius: 50% 50%;'/>")
        except:
            return format_html(
            f"<div width='120' height='120' style='border-radius: 50% 50%;'></div>")


PersonAdmin.highlight_deleted_field.short_description = PersonAdmin.field_to_highlight


@admin.register(Tatoo)
class TatooAdmin(SafeDeleteAdmin, GuardedModelAdmin):
    list_display = (highlight_deleted, "highlight_deleted_field", "uuid", "label", "foto_preview", "created_at",
                    "deleted_by") + SafeDeleteAdmin.list_display
    readonly_fields = ['foto_preview']
    list_filter = ("created_by", SafeDeleteAdminFilter,) + SafeDeleteAdmin.list_filter
    exclude = ()
    field_to_highlight = "id"

    def foto_preview(self, obj):
        try:
            return format_html(
            f"<img src='{obj.file.url}' width='120' height='120' style='border-radius: 50% 50%;'/>")
        except:
            return format_html(
            f"<div width='120' height='120' style='border-radius: 50% 50%;'></div>")


TatooAdmin.highlight_deleted_field.short_description = TatooAdmin.field_to_highlight


@admin.register(Nickname)
class NicknameAdmin(SafeDeleteAdmin, GuardedModelAdmin):
    list_display = (highlight_deleted, "highlight_deleted_field", "uuid", "label", "created_at",
                    "deleted_by") + SafeDeleteAdmin.list_display
    list_filter = ("created_by", SafeDeleteAdminFilter,) + SafeDeleteAdmin.list_filter
    exclude = ()
    field_to_highlight = "id"


NicknameAdmin.highlight_deleted_field.short_description = NicknameAdmin.field_to_highlight


@admin.register(Physical)
class PhysicalAdmin(SafeDeleteAdmin, GuardedModelAdmin):
    list_display = (highlight_deleted, "highlight_deleted_field", "uuid", "label", "value", "created_at",
                    "deleted_by") + SafeDeleteAdmin.list_display
    list_filter = ("created_by", SafeDeleteAdminFilter,) + SafeDeleteAdmin.list_filter
    exclude = ()
    field_to_highlight = "id"


PhysicalAdmin.highlight_deleted_field.short_description = PhysicalAdmin.field_to_highlight
