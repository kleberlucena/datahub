from django.contrib import admin

from apps.rpa_manager.models import (
    Missao,
    Aeronave,
    Checklist,
    Relatorio,
    HistoricoAlteracoesAeronave,
    Bateria,
    NaturezaDeVoo,
    TipoDeOperacao,
    CidadesPB,
    Guarnicao,
    Incidentes,
    Entidades,
    PontosDeInteresse,
    ImagensIncidente,
    ImagensChecklist,
    Legislation,
    Severity,
    Probability,
    Tolerability,
    Situation,
    Assessment,
    RiskAssessment
)

class MissaoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'usuario','concluida', 'horario', 'data')
    
class GuarnicaoAdmin(admin.ModelAdmin):
    list_display = ('motorista', 'piloto_remoto','telefone', 'local', 'data')
    
class HistoricoAlteracoesAeronaveAdmin(admin.ModelAdmin):
    list_display = ('aeronave', 'alteracoes', 'data', 'codigo')

class AeronaveAdmin(admin.ModelAdmin):
    list_display = ('prefixo', 'modelo', 'marca')

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
admin.site.register(Checklist, ChecklistAdmin)
admin.site.register(Relatorio, RelatorioAdmin)
admin.site.register(HistoricoAlteracoesAeronave, HistoricoAlteracoesAeronaveAdmin)
admin.site.register(Guarnicao, GuarnicaoAdmin)
admin.site.register(Bateria)
admin.site.register(NaturezaDeVoo)
admin.site.register(TipoDeOperacao)
admin.site.register(CidadesPB)
admin.site.register(Incidentes)
admin.site.register(Entidades)
admin.site.register(Legislation)
admin.site.register(PontosDeInteresse)
admin.site.register(ImagensIncidente)
admin.site.register(Severity)
admin.site.register(Probability)
admin.site.register(Tolerability)
admin.site.register(Situation)
admin.site.register(Assessment)
admin.site.register(RiskAssessment)
