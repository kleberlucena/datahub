from django.contrib import admin

from apps.document.models import Document
from safedelete.admin import SafeDeleteAdmin, SafeDeleteAdminFilter, highlight_deleted

@admin.register(Document)
class DocumentAdmin(SafeDeleteAdmin):
    list_display = (highlight_deleted, "highlight_deleted_field", "created_at",
                    "deleted_by") + SafeDeleteAdmin.list_display
    list_filter = ("created_by", SafeDeleteAdminFilter,) + SafeDeleteAdmin.list_filter
    exclude = ()
    field_to_highlight = "id"


DocumentAdmin.highlight_deleted_field.short_description = DocumentAdmin.field_to_highlight

