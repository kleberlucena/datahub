from django.contrib import admin
from guardian.admin import GuardedModelAdmin
from apps.document.models import Document, DocumentType, DocumentImage
from safedelete.admin import SafeDeleteAdmin, SafeDeleteAdminFilter, highlight_deleted
from django.utils.html import format_html


@admin.register(DocumentType)
class DocumentTypeAdmin(SafeDeleteAdmin, GuardedModelAdmin):
    list_display = (highlight_deleted, "highlight_deleted_field", "label", "emitter_department", "created_at",
                    "deleted_by") + SafeDeleteAdmin.list_display
    list_filter = ("created_by", "updated_by", SafeDeleteAdminFilter,) + SafeDeleteAdmin.list_filter
    exclude = ()
    field_to_highlight = "id"

    @admin.action(description='Add deleted_by on deleted objects')
    def delete_model(self, request, obj):
        user = request.user
        obj.delete(deleted_by=user)


DocumentTypeAdmin.highlight_deleted_field.short_description = DocumentTypeAdmin.field_to_highlight


@admin.register(DocumentImage)
class DocumentImageAdmin(SafeDeleteAdmin, GuardedModelAdmin):
    list_display = (highlight_deleted, "highlight_deleted_field", "foto_preview", "created_at",
                    "deleted_by") + SafeDeleteAdmin.list_display
    readonly_fields = ['foto_preview']
    list_filter = ("created_by", SafeDeleteAdminFilter,) + SafeDeleteAdmin.list_filter
    exclude = ()
    field_to_highlight = "id"

    @admin.action(description='Add deleted_by on deleted objects')
    def delete_model(self, request, obj):
        user = request.user
        obj.delete(deleted_by=user)

    def foto_preview(self, obj):
        return format_html(
            f"<img src='{obj}' width='120' height='120' style='border-radius: 50% 50%;'/>")


DocumentImageAdmin.highlight_deleted_field.short_description = DocumentImageAdmin.field_to_highlight


@admin.register(Document)
class DocumentAdmin(SafeDeleteAdmin, GuardedModelAdmin):
    list_display = (highlight_deleted, "highlight_deleted_field", "name", "number", "created_at",
                    "deleted_by") + SafeDeleteAdmin.list_display
    list_filter = ("created_by", SafeDeleteAdminFilter,) + SafeDeleteAdmin.list_filter
    exclude = ()
    field_to_highlight = "id"

    @admin.action(description='Add deleted_by on deleted objects')
    def delete_model(self, request, obj):
        user = request.user
        obj.delete(deleted_by=user)


DocumentAdmin.highlight_deleted_field.short_description = DocumentAdmin.field_to_highlight

