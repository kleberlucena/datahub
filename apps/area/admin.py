from django.contrib import admin
from django.contrib.gis import admin as geo_admin

from apps.area.models import *


@admin.register(Area)
class AreaAdmin(geo_admin.OSMGeoAdmin):
    list_display = ('name', "description", "area_polygon")