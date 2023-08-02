from django.contrib import admin
from django.utils.html import format_html
from guardian.admin import GuardedModelAdmin
from safedelete.admin import SafeDeleteAdmin, SafeDeleteAdminFilter, highlight_deleted

from .models import Fact, FactType, FactImage
from apps.person.models import Person

@admin.register(FactType)
class FactTypeAdmin(SafeDeleteAdmin, GuardedModelAdmin):
    list_display = (highlight_deleted, "highlight_deleted_field", "title", "description", "created_at",
                    "deleted_by") + SafeDeleteAdmin.list_display
    list_filter = ("title", "description", "created_at", SafeDeleteAdminFilter,) + SafeDeleteAdmin.list_filter
    exclude = ()
    field_to_highlight = "id"

    @admin.action(description='Add deleted_by on deleted objects')
    def delete_model(self, request, obj):
        user = request.user
        obj.delete(deleted_by=user)


FactTypeAdmin.highlight_deleted_field.short_description = FactTypeAdmin.field_to_highlight


@admin.register(FactImage)
class FactImageAdmin(SafeDeleteAdmin, GuardedModelAdmin):
    list_display = (highlight_deleted, "highlight_deleted_field", "label", "fact", "entity", "foto_preview", "created_at",
                    "created_by", "deleted_by") + SafeDeleteAdmin.list_display
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
    

FactImageAdmin.highlight_deleted_field.short_description = FactImageAdmin.field_to_highlight


class VictimsAdminInLine(admin.TabularInline):
    model = Fact.victims.through


class SuspectsAdminInLine(admin.TabularInline):
    model = Fact.suspects.through


class WitnessesAdminInLine(admin.TabularInline):
    model = Fact.witnesses.through


class AddressesAdminInLine(admin.TabularInline):
    model = Fact.addresses.through


class FactImagesAdminInLine(admin.TabularInline):
    model = FactImage


@admin.register(Fact)
class FactAdmin(SafeDeleteAdmin, GuardedModelAdmin):
    list_display = (highlight_deleted, "highlight_deleted_field", 'uuid', 'title', 'description', 'fact_type', 'entity', 'start_time', 'end_time', 'created_at', 'updated_at',
                    "created_by", "deleted_by") + SafeDeleteAdmin.list_display
    inlines = [
        VictimsAdminInLine, SuspectsAdminInLine, WitnessesAdminInLine, AddressesAdminInLine, FactImagesAdminInLine
    ]
    list_filter = ("created_by", SafeDeleteAdminFilter,) + SafeDeleteAdmin.list_filter
    search_fields = ('uuid', 'created_at', 'updated_at')
    exclude = ()
    field_to_highlight = "id"

    @admin.action(description='Add deleted_by on deleted objects')
    def delete_model(self, request, obj):
        user = request.user
        obj.delete(deleted_by=user)


FactAdmin.highlight_deleted_field.short_description = FactAdmin.field_to_highlight
