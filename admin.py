from django.contrib import admin
from .models import Incident, Guns, Vehicles, Drug, Local
from .models import SupportingNI, OstensiveArresting, OccurrenceNature, NiIndication, DriRegion

class IncidentAdmin(admin.ModelAdmin):
    list_display = ('CCD_key', 'timestamp')

class GunsAdmin(admin.ModelAdmin):
    list_display = ('incident',)

class VehiclesAdmin(admin.ModelAdmin):
    list_display = ('incident',)

class DrugAdmin(admin.ModelAdmin):
    list_display = ('incident',)

class SupportingNIAdmin(admin.ModelAdmin):
    list_display = ['name']

class OstensiveArrestingAdmin(admin.ModelAdmin):
    list_display = ['name']

class OccurrenceNatureAdmin(admin.ModelAdmin):
    list_display = ['name']

class NiIndicationAdmin(admin.ModelAdmin):
    list_display = ['name']

class DriRegionAdmin(admin.ModelAdmin):
    list_display = ['name']

class LocalAdmin(admin.ModelAdmin):
    class Media:
        js = ['/plugins/jquery/local_map.js']

admin.site.register(Incident, IncidentAdmin)
admin.site.register(Guns, GunsAdmin)
admin.site.register(Vehicles, VehiclesAdmin)
admin.site.register(Drug, DrugAdmin)
admin.site.register(SupportingNI, SupportingNIAdmin)
admin.site.register(OstensiveArresting, OstensiveArrestingAdmin)
admin.site.register(OccurrenceNature, OccurrenceNatureAdmin)
admin.site.register(NiIndication, NiIndicationAdmin)
admin.site.register(DriRegion, DriRegionAdmin)
admin.site.register(Local, LocalAdmin)
