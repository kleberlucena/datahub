from django.contrib import admin
from django.contrib.gis import admin as geo_admin

from apps.radio.models import *


@admin.register(Gps)
class GpsAdmin(geo_admin.OSMGeoAdmin):
    list_display = ('uuid', "location", "accuracy", "id", "created_at",
                    "timestamp", "timestampReceived")
    field_to_highlight = "id"
