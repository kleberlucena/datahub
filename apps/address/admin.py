from django.contrib import admin
from django.contrib.gis import admin as geo_admin
from safedelete.admin import SafeDeleteAdmin, SafeDeleteAdminFilter, highlight_deleted

from apps.address.models import *


@admin.register(Address)
class AddressAdmin(SafeDeleteAdmin, geo_admin.ModelAdmin):
    list_display = ('uuid', highlight_deleted, "highlight_deleted_field", "created",
                    "deleted_by") + SafeDeleteAdmin.list_display
    list_filter = ("created_by", SafeDeleteAdminFilter,) + SafeDeleteAdmin.list_filter
    exclude = ()
    field_to_highlight = "id"


AddressAdmin.highlight_deleted_field.short_description = AddressAdmin.field_to_highlight
