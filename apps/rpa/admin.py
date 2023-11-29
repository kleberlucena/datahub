from django.contrib import admin

from apps.rpa.models import *

class OperationAdmin(admin.ModelAdmin):
    list_display = ('title', 'user','completed', 'time', 'date')
    
class PoliceGroupAdmin(admin.ModelAdmin):
    list_display = ('entity', 'driver', 'remote_pilot','phone', 'location', 'date')
    
class AircraftHistoricAdmin(admin.ModelAdmin):
    list_display = ('aircraft', 'changes', 'date', 'code')

class AircraftAdmin(admin.ModelAdmin):
    list_display = ('prefix', 'model', 'brand')

class ChecklistAdmin(admin.ModelAdmin):
    list_display = ('aircraft', 'remote_pilot', 'date', 'changes')

class ReportAdmin(admin.ModelAdmin):
    list_display = ('title', 'remote_pilot', 'date', 'aircraft')

class MilitarAdmin(admin.ModelAdmin):
    list_display = ('nome_de_guerra', 'total_de_horas_voo', 'matricula',  'display_roles')

    def display_roles(self, obj):
        return ", ".join([role.role for role in obj.roles.all()])

admin.site.register(Operation, OperationAdmin)
admin.site.register(Aircraft, AircraftAdmin)
admin.site.register(Checklist, ChecklistAdmin)
admin.site.register(Report, ReportAdmin)
admin.site.register(AicraftHistoric, AircraftHistoricAdmin)
admin.site.register(PoliceGroup, PoliceGroupAdmin)
admin.site.register(Battery)
admin.site.register(FlightNature)
admin.site.register(TypesOfOperations)
admin.site.register(CitiesPB)
admin.site.register(Incidents)
admin.site.register(Legislation)
admin.site.register(PointsOfInterest)
admin.site.register(IncidentImage)
admin.site.register(Severity)
admin.site.register(Probability)
admin.site.register(Tolerability)
admin.site.register(Situation)
admin.site.register(Assessment)
admin.site.register(RiskAssessment)

