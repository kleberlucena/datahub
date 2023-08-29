from django.contrib import admin

from . import models


@admin.register(models.PersonBNMP)
class PersonBNMPAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'idpessoa', 'numeroCPF', 'nome', 'nomeMae', 'dataNascimento')
    search_fields = ('uuid',)


@admin.register(models.RegistryBNMP)
class RegistryBNMPAdmin(admin.ModelAdmin):
    list_display = ('person', 'person_bnmp')
    search_fields = ('person_uuid', 'person_bnmp_uuid')
    readonly_fields = ('person_uuid', 'person_bnmp_uuid', 'person_info', 'person_bnmp_numeroCPF', 'person_bnmp_nome', 'person_bnmp_alcunha', 'person_bnmp_nomeMae', 'person_bnmp_dataNascimento')

    def person_uuid(self, obj):
        return obj.person.uuid
    person_uuid.short_description = 'Person UUID'

    def person_bnmp_uuid(self, obj):
        return obj.person_bnmp.uuid
    person_bnmp_uuid.short_description = 'Person BNMP UUID'

    def person_info(self, obj):
        person = obj.person
        return f"UUID: {person.uuid}, Other fields: ..."  # Display other relevant fields
    person_info.short_description = 'Person Info'

    def person_bnmp_info(self, obj):
        person_bnmp = obj.person_bnmp
        return f"UUID: {person_bnmp.uuid}, Other fields: ..."  # Display other relevant fields
    person_bnmp_info.short_description = 'Person BNMP Info'
    
    def person_bnmp_numeroCPF(self, obj):
        try:
            return obj.person_bnmp.numeroCPF
        except:
            return None
        
    def person_bnmp_nome(self, obj):
        try:
            return obj.person_bnmp.nome
        except:
            return None
        
    def person_bnmp_alcunha(self, obj):
        try:
            return obj.person_bnmp.alcunha
        except:
            return None
        
    def person_bnmp_nomeMae(self, obj):
        try:
            return obj.person_bnmp.nomeMae
        except:
            return None
        
    def person_bnmp_dataNascimento(self, obj):
        try:
            return obj.person_bnmp.dataNascimento
        except:
            return None