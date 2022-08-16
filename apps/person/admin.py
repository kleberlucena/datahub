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
    list_display = (highlight_deleted, "highlight_deleted_field", 'uuid', 'created_at',
                    'updated_at', "created_by", "deleted_by") + SafeDeleteAdmin.list_display
    list_filter = ("created_by", SafeDeleteAdminFilter,) + SafeDeleteAdmin.list_filter
    search_fields = ('uuid',)
    exclude = ()
    field_to_highlight = "id"


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
        return format_html(
            f"<img src='{obj}' width='120' height='120' style='border-radius: 50% 50%;'/>")


TatooAdmin.highlight_deleted_field.short_description = TatooAdmin.field_to_highlight


@admin.register(Nickname)
class NicknameAdmin(SafeDeleteAdmin, GuardedModelAdmin):
    list_display = (highlight_deleted, "highlight_deleted_field", "uuid", "nickname", "created_at",
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


# @admin.register(PersonDocument)
# class PersonDocumentAdmin(admin.ModelAdmin):
#     list_display = ('uuid', 'person', 'created', 'updated')
#     search_fields = ('uuid', 'person')
#
#
# @admin.register(PersonNickname)
# class PersonNicknameAdmin(admin.ModelAdmin):
#     list_display = ('uuid', 'nickname', 'person', 'created', 'updated')
#     search_fields = ('uuid',)
#
#
# @admin.register(PersonAddress)
# class PersonAddressAdmin(admin.ModelAdmin):
#     list_display = ('uuid', 'address', 'created', 'updated')
#     search_fields = ('uuid',)
#
#
# @admin.register(PersonImage)
# class PersonImageAdmin(admin.ModelAdmin):
#     list_display = ('uuid', 'person', 'foto_preview', 'image', 'created', 'updated')
#     readonly_fields = ['foto_preview']
#     search_fields = ('uuid',)
#
#     def foto_preview(self, obj):
#         return format_html(
#             f"<img src='{obj.image}' width='120' height='120' style='border-radius: 50% 50%;'/>")
#
#
# @admin.register(PersonImageFace)
# class PersonImageFaceAdmin(admin.ModelAdmin):
#     list_display = ('uuid', 'person', 'foto_preview', 'created', 'updated')
#     readonly_fields = ['foto_preview']
#     search_fields = ('uuid',)
#
#     def foto_preview(self, obj):
#         return format_html(
#             f"<img src='{obj.image}' width='120' height='120' style='border-radius: 50% 50%;'/>")
