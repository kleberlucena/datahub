from django.contrib import admin

from apps.rpa_manager.models import *


class MissaoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'usuario','concluida', 'horario', 'data')

class AeronaveAdmin(admin.ModelAdmin):
    list_display = ('prefixo', 'modelo', 'marca', 'maleta')

class ChecklistAdmin(admin.ModelAdmin):
    list_display = ('aeronave', 'piloto', 'data', 'alteracoes')

class RelatorioAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'militar', 'data', 'aeronave')

admin.site.register(Missao, MissaoAdmin)
admin.site.register(Aeronave, AeronaveAdmin)
admin.site.register(Maleta)
admin.site.register(Militar)
admin.site.register(Bateria)
admin.site.register(Checklist, ChecklistAdmin)
admin.site.register(OPM)
admin.site.register(Unidades)
admin.site.register(NaturezaDeVoo)
admin.site.register(TipoDeOperacao)
admin.site.register(Relatorio, RelatorioAdmin)
admin.site.register(CidadesPB)
