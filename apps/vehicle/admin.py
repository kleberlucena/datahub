from django.contrib import admin
from django.utils.html import format_html
from guardian.admin import GuardedModelAdmin
from safedelete.admin import SafeDeleteAdmin, SafeDeleteAdminFilter, highlight_deleted

from  .import models
from apps.person.models import Person


class ProprietarioAdminInLine(admin.TabularInline):
    model = models.PersonRenavamCortex


class PossuidorAdminInLine(admin.TabularInline):
    model = models.PersonRenavamCortex


class ArrendatarioAdminInLine(admin.TabularInline):
    model = models.PersonRenavamCortex


class ImagesAdminInLine(admin.TabularInline):
    model = models.VehicleImage


@admin.register(models.VehicleCortex)
class VehicleCortexAdmin(admin.ModelAdmin):
    list_display = ("uuid", "placa", "dataEmplacamento", "chassi", "tipoDocumentoFaturado", "numeroIdentificacaoFaturado", 
                  "ufEmplacamento", "tipoDocumentoProprietario", "ufEmplacamento", "municipioPlaca", "anoFabricacao", "anoModelo", 
                  "marcaModelo", "grupoVeiculo", "tipoVeiculo", "especie", "carroceria", "numeroCarroceria", "cor", 
                  "combustivel", "potencia", "cilindrada", "lotacao", "capacidadeMaximaCarga", "pesoBrutoTotal", 
                  "capacidadeMaximaTracao", "indicadorRemarcacaoChassi", "numeroCaixaCambio", "quantidadeEixo", "numeroEixoTraseiro",
                  "numeroEixoAuxiliar", "numeroMotor", "tipoMontagem", "numeroIdentificacaoImportador", "numeroDeclaracaoImportacao",
                  "dataDeclaracaoImportacao", "codigoOrgaoSRF", "dataDeclaracaoImportacao", "restricaoVeiculo1", "restricaoVeiculo2", 
                  "restricaoVeiculo3", "restricaoVeiculo4", "dataLimiteRestricaoTributaria", "indicadorVeiculoLicenciadoCirculacao", 
                  "renavam", "codigoMunicipioEmplacamento", "dataAtualizacaoRouboFurto", "dataAtualizacaoAlarme", 
                  "indicadorVeiculoNacional", "numeroLicencaUsoConfiguracaoVeiculosMotor", "categoria", "codigoCategoria", 
                  "dataEmissaoUltimoCRV", "dataHoraAtualizacaoVeiculo", "numeroProcessoImportacao", "paisTransferenciaVeiculo", 
                  "origemPossuidor", "registroAduaneiro", "situacaoVeiculo", 
                  "codigoMarcaModelo", "codigoEspecie", "codigoTipoVeiculo", "codigoCor", "restricao", 
                  "proprietario", "possuidor", "arrendatario", "created_at", "updated_at")
    
    list_filter = ("ufEmplacamento", "municipioPlaca", "anoFabricacao", "anoModelo", "marcaModelo","updated_at",)
    search_fields = ('uuid', 'placa', 'renavam', 'chassi', 'ufEmplacamento')
    exclude = ()
    field_to_highlight = "placa"


@admin.register(models.Vehicle)
class VehicleAdmin(SafeDeleteAdmin, GuardedModelAdmin):
    list_display = ('uuid', 'signal', 'chassi', 'owner', 'custodian', 'renter', 'uuid', 'created_at', 'updated_at',
                    "created_by", "deleted_by") + SafeDeleteAdmin.list_display
    inlines = [ ImagesAdminInLine, ]
    list_filter = ("created_by", SafeDeleteAdminFilter,) + SafeDeleteAdmin.list_filter
    search_fields = ('uuid', 'created_at', 'updated_at')
    exclude = ()
    field_to_highlight = "signal"

    @admin.action(description='Add deleted_by on deleted objects')
    def delete_model(self, request, obj):
        user = request.user
        obj.delete(deleted_by=user)

VehicleAdmin.highlight_deleted_field.short_description = VehicleAdmin.field_to_highlight


@admin.register(models.RegistryVehicleCortex)
class RegistryVehicleCortexAdmin(admin.ModelAdmin):
    list_display = ('person', 'person_renavam_cortex')
    search_fields = ('person_uuid', 'person_renavam_cortex_uuid')
    readonly_fields = ('person_uuid', 'person_renavam_cortex_uuid', 'person_info', 'person_renavam_tipoDocumento', 'person_renavam_numeroDocumento', 'person_renavam_nome', 'person_renavam_endereco')

    def person_uuid(self, obj):
        return obj.person.uuid
    person_uuid.short_description = 'Person UUID'

    def person_renavam_cortex_uuid(self, obj):
        return obj.person_renavam_cortex.uuid
    person_renavam_cortex_uuid.short_description = 'Person Renavam UUID'

    def person_info(self, obj):
        person = obj.person
        return f"UUID: {person.uuid}, Other fields: ..."  # Display other relevant fields
    person_info.short_description = 'Person Info'

    def person_renavam_cortex_info(self, obj):
        person_renavam_cortex = obj.person_renavam_cortex
        return f"UUID: {person_renavam_cortex.uuid}, Other fields: ..."  # Display other relevant fields
    person_renavam_cortex_info.short_description = 'Person Renavam Info'
    
    def person_renavam_numeroDocumento(self, obj):
        try:
            return obj.person_renavam_cortex.numeroDocumento
        except:
            return None
        
    def person_renavam_nome(self, obj):
        try:
            return obj.person_renavam_cortex.nome
        except:
            return None
        
    def person_renavam_tipoDocumento(self, obj):
        try:
            return obj.person_renavam_cortex.tipoDocumento
        except:
            return None
        
    def person_renavam_endereco(self, obj):
        try:
            return obj.person_renavam_cortex.endereco
        except:
            return None