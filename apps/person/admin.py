from django.contrib import admin
from django.utils.html import format_html
from guardian.admin import GuardedModelAdmin
from safedelete.admin import SafeDeleteAdmin, SafeDeleteAdminFilter, highlight_deleted

from apps.person.models import *


class FacesAdminInLine(admin.TabularInline):
    model = Face


class TattoosAdminInLine(admin.TabularInline):
    model = Tattoo


class NicknamesAdminInLine(admin.TabularInline):
    model = Nickname


class AddressesAdminInLine(admin.TabularInline):
    model = Person.addresses.through


class DocumentsAdminInLine(admin.TabularInline):
    model = Person.documents.through


class ImagesAdminInLine(admin.TabularInline):
    model = Person.images.through


@admin.register(Person)
class PersonAdmin(SafeDeleteAdmin, GuardedModelAdmin):
    list_display = (highlight_deleted, "highlight_deleted_field", 'uuid', 'created_at', 'updated_at',
                    "created_by", "deleted_by") + SafeDeleteAdmin.list_display
    inlines = [
        AddressesAdminInLine, DocumentsAdminInLine, ImagesAdminInLine,
        FacesAdminInLine, NicknamesAdminInLine, TattoosAdminInLine
    ]
    list_filter = ("created_by", SafeDeleteAdminFilter,) + SafeDeleteAdmin.list_filter
    search_fields = ('uuid', 'created_at', 'updated_at')
    exclude = ()
    field_to_highlight = "id"

    @admin.action(description='Add deleted_by on deleted objects')
    def delete_model(self, request, obj):
        user = request.user
        obj.delete(deleted_by=user)


PersonAdmin.highlight_deleted_field.short_description = PersonAdmin.field_to_highlight


@admin.register(Face)
class FaceAdmin(SafeDeleteAdmin, GuardedModelAdmin):
    list_display = (highlight_deleted, 'highlight_deleted_field', 'uuid', 'foto_preview', 'created_at',
                    'updated_at', 'created_by', 'deleted_by', 'person') + SafeDeleteAdmin.list_display
    list_filter = ("created_by", SafeDeleteAdminFilter,) + SafeDeleteAdmin.list_filter
    search_fields = ('uuid',)
    exclude = ()
    field_to_highlight = "id"

    @admin.action(description='Add deleted_by on deleted objects')
    def delete_model(self, request, obj):
        user = request.user
        obj.delete(deleted_by=user)

    def foto_preview(self, obj):
        try:
            return format_html(
            f"<img src='{obj.file.url}' width='120' height='120' style='border-radius: 50% 50%;'/>")
        except:
            return format_html(
            f"<div width='120' height='120' style='border-radius: 50% 50%;'></div>")


PersonAdmin.highlight_deleted_field.short_description = PersonAdmin.field_to_highlight


@admin.register(Tattoo)
class TattooAdmin(SafeDeleteAdmin, GuardedModelAdmin):
    list_display = (highlight_deleted, 'highlight_deleted_field', 'uuid', 'label', 'point',  'foto_preview',
                    'person', 'created_at', 'created_by', 'deleted_by') + SafeDeleteAdmin.list_display
    readonly_fields = ['foto_preview']
    list_filter = ('created_by', 'created_at', SafeDeleteAdminFilter,) + SafeDeleteAdmin.list_filter
    exclude = ()
    field_to_highlight = "id"

    @admin.action(description='Add deleted_by on deleted objects')
    def delete_model(self, request, obj):
        user = request.user
        obj.delete(deleted_by=user)

    def foto_preview(self, obj):
        try:
            return format_html(
            f"<img src='{obj.file.url}' width='120' height='120' style='border-radius: 50% 50%;'/>")
        except:
            return format_html(
            f"<div width='120' height='120' style='border-radius: 50% 50%;'></div>")


TattooAdmin.highlight_deleted_field.short_description = TattooAdmin.field_to_highlight


@admin.register(Nickname)
class NicknameAdmin(SafeDeleteAdmin, GuardedModelAdmin):
    list_display = (highlight_deleted, "highlight_deleted_field", "uuid", "label", "created_at",
                    "deleted_by") + SafeDeleteAdmin.list_display
    list_filter = ("created_by", SafeDeleteAdminFilter,) + SafeDeleteAdmin.list_filter
    exclude = ()
    field_to_highlight = "id"

    @admin.action(description='Add deleted_by on deleted objects')
    def delete_model(self, request, obj):
        user = request.user
        obj.delete(deleted_by=user)


NicknameAdmin.highlight_deleted_field.short_description = NicknameAdmin.field_to_highlight


@admin.register(Physical)
class PhysicalAdmin(SafeDeleteAdmin, GuardedModelAdmin):
    list_display = (highlight_deleted, "highlight_deleted_field", "uuid", "label", "value", "created_at",
                    "deleted_by") + SafeDeleteAdmin.list_display
    list_filter = ("created_by", SafeDeleteAdminFilter,) + SafeDeleteAdmin.list_filter
    exclude = ()
    field_to_highlight = "id"

    @admin.action(description='Add deleted_by on deleted objects')
    def delete_model(self, request, obj):
        user = request.user
        obj.delete(deleted_by=user)


@admin.register(Registry)
class RegistryAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'system_label', 'person')
    search_fields = ('system_label',)


PhysicalAdmin.highlight_deleted_field.short_description = PhysicalAdmin.field_to_highlight
