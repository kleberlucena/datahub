from django.contrib import admin
from django.contrib.gis import admin as geo_admin

from apps.georeference.models import *


@admin.register(Area)
class AreaAdmin(geo_admin.OSMGeoAdmin):
    list_display = ('name', "description", "area_polygon")

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', "description")