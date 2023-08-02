from django.contrib import admin
from django.utils.html import format_html


from apps.portal import models


@admin.register(models.Entity)
class UnitsJsonFromApiAdmin(admin.ModelAdmin):
    fields = ('name', 'category', 'hierarchy')
    readonly_fields = ('created_at',)
    search_fields = ('name',)


""" @admin.register(models.Military)
class MilitaryJsonFromApiAdmin(admin.ModelAdmin):
    fields = ("entity", "name", "nickname", "admission_date",
              "birthdate", "register", "activity_status", "cpf", "genre", "email", "father", "mather", "place_of_birth", "marital_status", "phone", "address", "number", "complement", "district", "city", "state", "zipcode", )
    readonly_fields = ('created_at',) """


@admin.register(models.HistoryTransfer)
class HistoryJsonFromApiAdmin(admin.ModelAdmin):
    fields = ('military', 'entity', 'date_start',
              'date_finish', 'obs', )
    readonly_fields = ('created_at',)


@admin.register(models.Promotion)
class PromotionJsonFromApiAdmin(admin.ModelAdmin):
    fields = ('military', 'rank',)
    readonly_fields = ('created_at',)


@admin.register(models.Military)
class MilitaryAdmin(admin.ModelAdmin):
    list_display = ("entity", "name", "nickname", "admission_date",
              "birthdate", "register", "activity_status", "cpf", "genre", "email", "father", "mather", "place_of_birth", "marital_status", "phone", "address", "number", "complement", "district", "city", "state", "zipcode", 'image', 'foto_preview')
    search_fields = ('name', 'register')
    readonly_fields = ('created_at',)
    
    def foto_preview(self, obj):
        try:
            return format_html(
            f"<img src='{obj.image.url}' width='120' height='120' />")
        except:
            return format_html(
            f"<div width='120' height='120' ></div>")
