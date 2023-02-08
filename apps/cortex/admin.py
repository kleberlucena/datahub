from django.contrib import admin

from . import models


@admin.register(models.PersonCortex)
class PersonCortexAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'dataAtualizacao', 'numeroCPF', 'nomeCompleto', 'nomeSocial', 'anoObito', 'sexo', 'ocupacaoPrincipal', 'nomeMae', 'dataNascimento', 'municipio', 'ddd', 'telefone', )
    search_fields = ('uuid',)