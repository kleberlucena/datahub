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
