from django.contrib import admin

from . import models


@admin.register(models.RegistryCortex)
class RegistryCortexAdmin(admin.ModelAdmin):
    list_display = ('person', 'person_cortex')
    search_fields = ('person_uuid', 'person_cortex_uuid')
    readonly_fields = ('person_uuid', 'person_cortex_uuid', 'person_info', 'person_cortex_numeroCPF', 'person_cortex_nomeCompleto', 'person_cortex_nomeMae', 'person_cortex_dataNascimento')

    def person_uuid(self, obj):
        return obj.person.uuid
    person_uuid.short_description = 'Person UUID'

    def person_cortex_uuid(self, obj):
        return obj.person_cortex.uuid
    person_cortex_uuid.short_description = 'Person Cortex UUID'

    def person_info(self, obj):
        person = obj.person
        return f"UUID: {person.uuid}, Other fields: ..."  # Display other relevant fields
    person_info.short_description = 'Person Info'

    def person_cortex_info(self, obj):
        person_cortex = obj.person_cortex
        return f"UUID: {person_cortex.uuid}, Other fields: ..."  # Display other relevant fields
    person_cortex_info.short_description = 'Person Cortex Info'

    # Include the fields from the related models
    #def get_fields(self, request, obj=None):
    #    fields = super().get_fields(request, obj)
    #    fields += ('person__uuid', 'person_cortex__numeroCPF', 'person_cortex__nomeCompleto', 'person_cortex__nomeMae', 'person_cortex__dataNascimento')
    #    return fields
    
    def person_cortex_numeroCPF(self, obj):
        try:
            return obj.person_cortex.numeroCPF
        except:
            return None
        
    def person_cortex_nomeCompleto(self, obj):
        try:
            return obj.person_cortex.nomeCompleto
        except:
            return None
        
    def person_cortex_nomeMae(self, obj):
        try:
            return obj.person_cortex.nomeMae
        except:
            return None
        
    def person_cortex_dataNascimento(self, obj):
        try:
            return obj.person_cortex.dataNascimento
        except:
            return None

@admin.register(models.PersonCortex)
class PersonCortexAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'dataAtualizacao', 'numeroCPF', 'nomeCompleto', 'nomeSocial', 'anoObito', 'sexo', 'ocupacaoPrincipal', 'nomeMae', 'dataNascimento', 'municipio', 'ddd', 'telefone', )
    search_fields = ('uuid', 'numeroCPF', 'nomeCompleto', 'nomeSocial')