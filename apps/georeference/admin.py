from django.contrib import admin
from django.contrib.gis import admin as geo_admin
from apps.georeference.models import *
from apps.georeference import models


@admin.register(Area)
class AreaAdmin(geo_admin.OSMGeoAdmin):
    list_display = ('name', "description", "area_polygon")

admin.site.register(models.Category)
admin.site.register(models.SpotType)
admin.site.register(models.Spot)
admin.site.register(models.SpotAddresses)
