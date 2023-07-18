from django.contrib import admin

from apps.rpa_manager.models import *


class MissaoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'usuario','concluida', 'horario', 'data')
    
class HistoricoAlteracoesAeronaveAdmin(admin.ModelAdmin):
    list_display = ('aeronave', 'alteracoes', 'data', 'codigo')

class AeronaveAdmin(admin.ModelAdmin):
    list_display = ('prefixo', 'modelo', 'marca', 'maleta')

class ChecklistAdmin(admin.ModelAdmin):
    list_display = ('aeronave', 'piloto', 'data', 'alteracoes')

class RelatorioAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'militar', 'data', 'aeronave')

class MilitarAdmin(admin.ModelAdmin):
    list_display = ('nome_de_guerra', 'total_de_horas_voo', 'matricula',  'display_roles')

    def display_roles(self, obj):
        return ", ".join([role.role for role in obj.roles.all()])

admin.site.register(Missao, MissaoAdmin)
admin.site.register(Aeronave, AeronaveAdmin)
admin.site.register(Militar, MilitarAdmin)
admin.site.register(Checklist, ChecklistAdmin)
admin.site.register(Relatorio, RelatorioAdmin)
admin.site.register(HistoricoAlteracoesAeronave, HistoricoAlteracoesAeronaveAdmin)
admin.site.register(Maleta)
admin.site.register(Bateria)
admin.site.register(OPM)
admin.site.register(Unidades)
admin.site.register(NaturezaDeVoo)
admin.site.register(TipoDeOperacao)
admin.site.register(CidadesPB)
admin.site.register(Roles)
