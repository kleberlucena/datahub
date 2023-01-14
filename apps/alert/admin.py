from django.contrib import admin

from . import models


@admin.register(models.AlertCortex)
class AlertCortexAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'person', 'dados')
    search_fields = ('uuid',)


@admin.register(models.VehicleAlertCortex)
class VehicleAlertCortexAdmin(admin.ModelAdmin):
    list_display = ('placa', 'latitudePassagem', 'longitudePassagem')
    search_fields = ('placa',)


@admin.register(models.PersonAlertCortex)
class PersonAlertCortexAdmin(admin.ModelAdmin):
    list_display = ('cpf', 'nome', 'dataNascimento', 'nomeMae')
    search_fields = ('cpf', 'nome')