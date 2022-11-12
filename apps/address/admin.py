from django.contrib import admin
from django.contrib.gis import admin as geo_admin
from safedelete.admin import SafeDeleteAdmin, SafeDeleteAdminFilter, highlight_deleted

from apps.address.models import *


@admin.register(Address)
class AddressAdmin(SafeDeleteAdmin, geo_admin.OSMGeoAdmin):
    list_display = ('uuid', highlight_deleted, "highlight_deleted_field", "created_at",
                    "deleted_by") + SafeDeleteAdmin.list_display
    list_filter = ("created_by", SafeDeleteAdminFilter,) + SafeDeleteAdmin.list_filter
    exclude = ()
    field_to_highlight = "id"

    @admin.action(description='Add deleted_by on deleted objects')
    def delete_model(self, request, obj):
        user = request.user
        obj.delete(deleted_by=user)


AddressAdmin.highlight_deleted_field.short_description = AddressAdmin.field_to_highlight
